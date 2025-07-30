from logging import Logger, getLogger
from typing import Optional


class AppHandler():

    def __init__(
        self,
        app_name: str = None,
        logger: Logger = None,
        test_mode: Optional[bool] = False
    ):
        self.app_name = app_name
        self.logger = logger
        self.__is_test__ = test_mode

    def __set_app_name__(self, app_name: str) -> None:
        self.app_name = app_name

    def __set_test_mode__(self) -> None:
        self.__is_test__ = True

    @classmethod
    def test(cls) -> 'AppHandler':
        return cls("test", getLogger("test"), test_mode=True)
