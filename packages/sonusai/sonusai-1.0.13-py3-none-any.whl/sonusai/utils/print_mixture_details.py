from collections.abc import Callable

from ..datatypes import ClassCount
from ..mixture.helpers import mixture_all_speech_metadata
from ..mixture.mixdb import MixtureDatabase


def print_mixture_details(
    mixdb: MixtureDatabase,
    mixid: int | None = None,
    print_fn: Callable = print,
) -> None:
    from ..utils.seconds_to_hms import seconds_to_hms

    if mixid is not None:
        if 0 < mixid >= mixdb.num_mixtures:
            raise ValueError(f"Given mixid is outside valid range of 0:{mixdb.num_mixtures - 1}.")

        print_fn(f"Mixture {mixid} details")
        mixture = mixdb.mixture(mixid)
        speech_metadata = mixture_all_speech_metadata(mixdb, mixture)
        for category, source in mixture.all_sources.items():
            source_file = mixdb.source_file(source.file_id)
            print_fn(f"  {category}")
            print_fn(f"    name: {source_file.name}")
            print_fn(f"    effects: {source.effects.to_dict()}")
            print_fn(f"    pre_tempo: {source.pre_tempo}")
            print_fn(f"    duration: {seconds_to_hms(source_file.duration)}")
            print_fn(f"    start: {source.start}")
            print_fn(f"    repeat: {source.repeat}")
            print_fn(f"    snr: {source.snr}")
            print_fn(f"    random_snr: {source.snr.is_random}")
            print_fn(f"    snr_gain: {source.snr_gain}")
            for key in source_file.truth_configs:
                print_fn(f"    truth '{key}' function: {source_file.truth_configs[key].function}")
                print_fn(f"    truth '{key}' config: {source_file.truth_configs[key].config}")
                print_fn(
                    f"    truth '{key}' stride_reduction: {source_file.truth_configs[key].stride_reduction}"
                )
            for key in speech_metadata[category]:
                print_fn(f"{category} speech {key}: {speech_metadata[category][key]}")
        print_fn(f"  samples: {mixture.samples}")
        print_fn(f"  feature frames: {mixdb.mixture_feature_frames(mixid)}")
        print_fn("")


def print_class_count(
    class_count: ClassCount,
    length: int,
    print_fn: Callable = print,
    all_class_counts: bool = False,
) -> None:
    from ..utils.max_text_width import max_text_width

    print_fn("Class count:")
    idx_len = max_text_width(len(class_count))
    for idx, count in enumerate(class_count):
        if all_class_counts or count > 0:
            desc = f"  class {idx + 1:{idx_len}}"
            print_fn(f"{desc:{length}} {count}")
