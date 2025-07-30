from finalsa.common.lambdas.app.AppEntry import AppEntry
from typing import Optional
from logging import Logger


class App(AppEntry):

    def __init__(
        self,
        app_name: Optional[str] = None,
        logger: Optional[Logger] = None,
        test_mode: Optional[bool] = False
    ) -> None:
        if logger is None:
            logger = Logger("root")
        super().__init__(app_name, logger)
        self.__is_test__ = test_mode

    def register(self, app_entry: AppEntry) -> None:
        app_entry.__set_app_name__(self.app_name)
        if self.__is_test__:
            app_entry.__set_test_mode__()
        self.sqs.__merge__(app_entry.sqs)
        self.http.__merge__(app_entry.http)
