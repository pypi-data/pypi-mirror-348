import functools
from typing import Any

import numpy as np
from pystoi import stoi

from ..constants import SAMPLE_RATE
from ..datatypes import AudioF
from ..datatypes import AudioStatsMetrics
from ..datatypes import AudioT
from ..datatypes import Segsnr
from ..datatypes import SpeechMetrics
from ..mixture.mixdb import MixtureDatabase
from ..utils.asr import calc_asr
from ..utils.db import linear_to_db
from .calc_audio_stats import calc_audio_stats
from .calc_pesq import calc_pesq
from .calc_phase_distance import calc_phase_distance
from .calc_segsnr_f import calc_segsnr_f
from .calc_segsnr_f import calc_segsnr_f_bin
from .calc_speech import calc_speech
from .calc_wer import calc_wer
from .calc_wsdr import calc_wsdr


def calculate_metrics(mixdb: MixtureDatabase, m_id: int, metrics: list[str], force: bool = False) -> dict[str, Any]:
    """Get metrics data for the given mixture ID

    :param mixdb: Mixture database object
    :param m_id: Zero-based mixture ID
    :param metrics: List of metrics to get
    :param force: Force computing data from original sources regardless of whether cached data exists
    :return: Dictionary of metric data
    """

    # Define cached functions for expensive operations
    @functools.lru_cache(maxsize=1)
    def mixture_sources() -> dict[str, AudioT]:
        return mixdb.mixture_sources(m_id)

    @functools.lru_cache(maxsize=1)
    def mixture_source() -> AudioT:
        return mixdb.mixture_source(m_id)

    @functools.lru_cache(maxsize=1)
    def mixture_source_f() -> AudioF:
        return mixdb.mixture_source_f(m_id)

    @functools.lru_cache(maxsize=1)
    def mixture_noise() -> AudioT:
        return mixdb.mixture_noise(m_id)

    @functools.lru_cache(maxsize=1)
    def mixture_noise_f() -> AudioF:
        return mixdb.mixture_noise_f(m_id)

    @functools.lru_cache(maxsize=1)
    def mixture_mixture() -> AudioT:
        return mixdb.mixture_mixture(m_id)

    @functools.lru_cache(maxsize=1)
    def mixture_mixture_f() -> AudioF:
        return mixdb.mixture_mixture_f(m_id)

    @functools.lru_cache(maxsize=1)
    def mixture_segsnr() -> Segsnr:
        return mixdb.mixture_segsnr(m_id)

    @functools.lru_cache(maxsize=1)
    def calculate_pesq() -> dict[str, float]:
        return {category: calc_pesq(mixture_mixture(), audio) for category, audio in mixture_sources().items()}

    @functools.lru_cache(maxsize=1)
    def calculate_speech() -> dict[str, SpeechMetrics]:
        return {
            category: calc_speech(mixture_mixture(), audio, calculate_pesq()[category])
            for category, audio in mixture_sources().items()
        }

    @functools.lru_cache(maxsize=1)
    def mixture_stats() -> AudioStatsMetrics:
        return calc_audio_stats(mixture_mixture(), mixdb.fg_info.ft_config.length / SAMPLE_RATE)

    @functools.lru_cache(maxsize=1)
    def sources_stats() -> dict[str, AudioStatsMetrics]:
        return {
            category: calc_audio_stats(audio, mixdb.fg_info.ft_config.length / SAMPLE_RATE)
            for category, audio in mixture_sources().items()
        }

    @functools.lru_cache(maxsize=1)
    def source_stats() -> AudioStatsMetrics:
        return calc_audio_stats(mixture_source(), mixdb.fg_info.ft_config.length / SAMPLE_RATE)

    @functools.lru_cache(maxsize=1)
    def noise_stats() -> AudioStatsMetrics:
        return calc_audio_stats(mixture_noise(), mixdb.fg_info.ft_config.length / SAMPLE_RATE)

    # Cache ASR configurations
    @functools.lru_cache(maxsize=32)
    def get_asr_config(asr_name: str) -> dict:
        value = mixdb.asr_configs.get(asr_name, None)
        if value is None:
            raise ValueError(f"Unrecognized ASR name: '{asr_name}'")
        return value

    # Cache ASR results for sources, source and mixture
    @functools.lru_cache(maxsize=16)
    def sources_asr(asr_name: str) -> dict[str, str]:
        return {
            category: calc_asr(audio, **get_asr_config(asr_name)).text for category, audio in mixture_sources().items()
        }

    @functools.lru_cache(maxsize=16)
    def source_asr(asr_name: str) -> str:
        return calc_asr(mixture_source(), **get_asr_config(asr_name)).text

    @functools.lru_cache(maxsize=16)
    def mixture_asr(asr_name: str) -> str:
        return calc_asr(mixture_mixture(), **get_asr_config(asr_name)).text

    def get_asr_name(m: str) -> str:
        parts = m.split(".")
        if len(parts) != 2:
            raise ValueError(f"Unrecognized format: '{m}'; must be of the form: '<metric>.<name>'")
        asr_name = parts[1]
        return asr_name

    def calc(m: str) -> Any:
        if m == "mxsnr":
            return {category: source.snr for category, source in mixdb.mixture(m_id).all_sources.items()}

        # Get cached data first, if exists
        if not force:
            value = mixdb.read_mixture_data(m_id, m)[m]
            if value is not None:
                return value

        # Otherwise, generate data as needed
        if m.startswith("mxwer"):
            asr_name = get_asr_name(m)

            if mixdb.mixture(m_id).is_noise_only:
                # noise only, ignore/reset target asr
                return float("nan")

            if source_asr(asr_name):
                return calc_wer(mixture_asr(asr_name), source_asr(asr_name)).wer * 100

            # TODO: should this be NaN like above?
            return float(0)

        if m.startswith("basewer"):
            asr_name = get_asr_name(m)

            text = mixdb.mixture_speech_metadata(m_id, "text")
            return {
                category: calc_wer(source, str(text[category])).wer * 100 if isinstance(text[category], str) else 0
                for category, source in sources_asr(asr_name).items()
            }

        if m.startswith("mxasr"):
            return mixture_asr(get_asr_name(m))

        if m == "mxssnr_avg":
            return calc_segsnr_f(mixture_segsnr()).avg

        if m == "mxssnr_std":
            return calc_segsnr_f(mixture_segsnr()).std

        if m == "mxssnr_avg_db":
            val = calc_segsnr_f(mixture_segsnr()).avg
            if val is not None:
                return linear_to_db(val)
            return None

        if m == "mxssnr_std_db":
            val = calc_segsnr_f(mixture_segsnr()).std
            if val is not None:
                return linear_to_db(val)
            return None

        if m == "mxssnrdb_avg":
            return calc_segsnr_f(mixture_segsnr()).db_avg

        if m == "mxssnrdb_std":
            return calc_segsnr_f(mixture_segsnr()).db_std

        if m == "mxssnrf_avg":
            return calc_segsnr_f_bin(mixture_source_f(), mixture_noise_f()).avg

        if m == "mxssnrf_std":
            return calc_segsnr_f_bin(mixture_source_f(), mixture_noise_f()).std

        if m == "mxssnrdbf_avg":
            return calc_segsnr_f_bin(mixture_source_f(), mixture_noise_f()).db_avg

        if m == "mxssnrdbf_std":
            return calc_segsnr_f_bin(mixture_source_f(), mixture_noise_f()).db_std

        if m == "mxpesq":
            if mixdb.mixture(m_id).is_noise_only:
                return dict.fromkeys(calculate_pesq(), 0)
            return calculate_pesq()

        if m == "mxcsig":
            if mixdb.mixture(m_id).is_noise_only:
                return dict.fromkeys(calculate_speech(), 0)
            return {category: s.csig for category, s in calculate_speech().items()}

        if m == "mxcbak":
            if mixdb.mixture(m_id).is_noise_only:
                return dict.fromkeys(calculate_speech(), 0)
            return {category: s.cbak for category, s in calculate_speech().items()}

        if m == "mxcovl":
            if mixdb.mixture(m_id).is_noise_only:
                return dict.fromkeys(calculate_speech(), 0)
            return {category: s.covl for category, s in calculate_speech().items()}

        if m == "mxwsdr":
            mixture = mixture_mixture()[:, np.newaxis]
            target = mixture_source()[:, np.newaxis]
            noise = mixture_noise()[:, np.newaxis]
            return calc_wsdr(
                hypothesis=np.concatenate((mixture, noise), axis=1),
                reference=np.concatenate((target, noise), axis=1),
                with_log=True,
            )[0]

        if m == "mxpd":
            return calc_phase_distance(hypothesis=mixture_mixture_f(), reference=mixture_source_f())[0]

        if m == "mxstoi":
            return stoi(
                x=mixture_source(),
                y=mixture_mixture(),
                fs_sig=SAMPLE_RATE,
                extended=False,
            )

        if m == "mxdco":
            return mixture_stats().dco

        if m == "mxmin":
            return mixture_stats().min

        if m == "mxmax":
            return mixture_stats().max

        if m == "mxpkdb":
            return mixture_stats().pkdb

        if m == "mxlrms":
            return mixture_stats().lrms

        if m == "mxpkr":
            return mixture_stats().pkr

        if m == "mxtr":
            return mixture_stats().tr

        if m == "mxcr":
            return mixture_stats().cr

        if m == "mxfl":
            return mixture_stats().fl

        if m == "mxpkc":
            return mixture_stats().pkc

        if m == "sdco":
            return {category: s.dco for category, s in sources_stats().items()}

        if m == "smin":
            return {category: s.min for category, s in sources_stats().items()}

        if m == "smax":
            return {category: s.max for category, s in sources_stats().items()}

        if m == "spkdb":
            return {category: s.pkdb for category, s in sources_stats().items()}

        if m == "slrms":
            return {category: s.lrms for category, s in sources_stats().items()}

        if m == "spkr":
            return {category: s.pkr for category, s in sources_stats().items()}

        if m == "str":
            return {category: s.tr for category, s in sources_stats().items()}

        if m == "scr":
            return {category: s.cr for category, s in sources_stats().items()}

        if m == "sfl":
            return {category: s.fl for category, s in sources_stats().items()}

        if m == "spkc":
            return {category: s.pkc for category, s in sources_stats().items()}

        if m == "mxsdco":
            return source_stats().dco

        if m == "mxsmin":
            return source_stats().min

        if m == "mxsmax":
            return source_stats().max

        if m == "mxspkdb":
            return source_stats().pkdb

        if m == "mxslrms":
            return source_stats().lrms

        if m == "mxspkr":
            return source_stats().pkr

        if m == "mxstr":
            return source_stats().tr

        if m == "mxscr":
            return source_stats().cr

        if m == "mxsfl":
            return source_stats().fl

        if m == "mxspkc":
            return source_stats().pkc

        if m.startswith("sasr"):
            return sources_asr(get_asr_name(m))

        if m.startswith("mxsasr"):
            return source_asr(get_asr_name(m))

        if m == "ndco":
            return noise_stats().dco

        if m == "nmin":
            return noise_stats().min

        if m == "nmax":
            return noise_stats().max

        if m == "npkdb":
            return noise_stats().pkdb

        if m == "nlrms":
            return noise_stats().lrms

        if m == "npkr":
            return noise_stats().pkr

        if m == "ntr":
            return noise_stats().tr

        if m == "ncr":
            return noise_stats().cr

        if m == "nfl":
            return noise_stats().fl

        if m == "npkc":
            return noise_stats().pkc

        if m == "sedavg":
            return 0

        if m == "sedcnt":
            return 0

        if m == "sedtop3":
            return np.zeros(3, dtype=np.float32)

        if m == "sedtopn":
            return 0

        if m == "ssnr":
            return mixture_segsnr()

        raise AttributeError(f"Unrecognized metric: '{m}'")

    result: dict[str, Any] = {}
    for metric in metrics:
        result[metric] = calc(metric)

        # Check for metrics dependencies and add them even if not explicitly requested.
        if metric.startswith("mxwer"):
            dependencies = ("mxasr." + metric[6:], "sasr." + metric[6:])
            for dependency in dependencies:
                result[dependency] = calc(dependency)

    return result
