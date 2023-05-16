import logging
from pathlib import Path

from app import start_bot
from utils import get_root_dir


def init_logger() -> None:
    # Create /logs dir if not exist
    log_dir = get_root_dir() + '/logs'
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Init Logger
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    file_handler = logging.FileHandler(log_dir + '/debug.log', 'a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging.DEBUG)


def main() -> None:
    init_logger()
    start_bot()


if __name__ == "__main__":
    main()
