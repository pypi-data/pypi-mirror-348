# -- import packages: ---------------------------------------------------------
import logging
import sys


# -- constants: ---------------------------------------------------------------
NAME = "adata_query"

# -- configure logger: --------------------------------------------------------
def configure_logging(name=NAME, log_file=f"{NAME}.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(
        logging.DEBUG
    )  # Keep at DEBUG to allow file handler to capture all levels

    # Prevent adding handlers multiple times (important in notebooks!)
    if logger.hasHandlers():
        return logger

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File handler (DEBUG+)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    stream_formatter = logging.Formatter(f"{NAME} [%(levelname)s]: %(message)s")

    # Stream handler (INFO+)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(stream_formatter)

    # Add filter to stream handler to only show INFO and above
    class InfoFilter(logging.Filter):
        def filter(self, record) -> bool:
            return record.levelno >= logging.INFO

    ch.addFilter(InfoFilter())

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
