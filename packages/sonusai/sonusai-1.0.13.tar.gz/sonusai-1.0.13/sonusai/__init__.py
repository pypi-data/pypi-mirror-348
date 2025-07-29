import logging
from importlib import metadata
from os.path import dirname

from rich.logging import RichHandler

__version__ = metadata.version(__package__)  # pyright: ignore [reportArgumentType]
BASEDIR = dirname(__file__)

commands_doc = """
   audiofe                      Audio front end
   calc_metric_spenh            Run speech enhancement and analysis
   doc                          Documentation
   genft                        Generate feature and truth data
   genmetrics                   Generate mixture metrics data
   genmix                       Generate mixture and truth data
   genmixdb                     Generate a mixture database
   lsdb                         List information about a mixture database
   metrics_summary              Summarize generated metrics in a mixture database
   mkwav                        Make WAV files from a mixture database
   onnx_predict                 Run ONNX predict on a trained model
   vars                         List custom SonusAI variables
"""

# create logger
logger = logging.getLogger("sonusai")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(message)s")
formatter_db = logging.Formatter("%(asctime)s %(message)s")
console_handler = RichHandler(show_level=False, show_path=False, show_time=False)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger_db = logging.getLogger("sonusai_db")
logger_db.setLevel(logging.DEBUG)

# create file handler
def create_file_handler(filename: str, verbose: bool = False) -> None:
    from pathlib import Path

    fh = logging.FileHandler(filename=filename, mode="w")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if verbose:
        filename_db = Path(filename)
        filename_db = filename_db.parent / (filename_db.stem + "_dbtrace" + filename_db.suffix)
        fh = logging.FileHandler(filename=filename_db, mode="w")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter_db)
        logger_db.addHandler(fh)


# update console handler
def update_console_handler(verbose: bool) -> None:
    if not verbose:
        logger.removeHandler(console_handler)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)


# write initial log message
def initial_log_messages(name: str, subprocess: str | None = None) -> None:
    from datetime import datetime
    from getpass import getuser
    from os import getcwd
    from socket import gethostname
    from sys import argv

    if subprocess is None:
        logger.info(f"SonusAI {__version__}")
    else:
        logger.info(f"SonusAI {subprocess}")
    logger.info(f"{name}")
    logger.info("")
    logger.debug(f"Host:      {gethostname()}")
    logger.debug(f"User:      {getuser()}")
    logger.debug(f"Directory: {getcwd()}")
    logger.debug(f"Date:      {datetime.now()}")
    logger.debug(f"Command:   {' '.join(argv)}")
    logger.debug("")


def commands_list(doc: str = commands_doc) -> list[str]:
    lines = doc.split("\n")
    commands = []
    for line in lines:
        command = line.strip().split(" ").pop(0)
        if command:
            commands.append(command)
    return commands


def exception_handler(e: Exception) -> None:
    import sys

    from rich.console import Console

    logger.error(f"{type(e).__name__}: {e}")
    handlers = [handler for handler in logger.handlers if isinstance(handler, logging.FileHandler)]
    logger.error(f"See {', '.join(handler.baseFilename for handler in handlers)} for details")

    console = Console(color_system=None)
    with console.capture() as capture:
        console.print_exception(show_locals=False)
    logger.debug(capture.get())
    sys.exit(1)
