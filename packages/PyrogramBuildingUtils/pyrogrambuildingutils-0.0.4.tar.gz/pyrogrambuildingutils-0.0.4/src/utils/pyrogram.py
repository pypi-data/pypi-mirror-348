import logging

from src.templates.envtemplate import build_env
from src.utils.utils import Utils

logging.basicConfig(level=logging.INFO)


class Init:
    logger = logging.getLogger("customPyrogram.init")

    @Utils.init_time_measure()
    def __init__(self) -> None:
        Utils.clear_pycache()
        self._run()

    def _run(self) -> None:
        build_env()


def run():
    Init()
