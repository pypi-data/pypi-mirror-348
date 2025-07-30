from finalsa.common.lambdas.sqs.SqsHandler import SqsHandler
from finalsa.common.lambdas.http.HttpHandler import HttpHandler
from typing import Optional, Union, Dict, Any, List
from finalsa.sqs.client import SqsServiceTest
from logging import Logger, getLogger


class AppEntry():

    def __init__(
        self,
        app_name: Optional[str] = None,
        logger: Optional[Logger] = None
    ) -> None:
        self.app_name = app_name
        if logger is None:
            logger = getLogger("root")
        self.__is_test__ = False
        self.sqs = SqsHandler(self.app_name, logger)
        self.http = HttpHandler(self.app_name, logger)

    def __set_app_name__(self, app_name: str) -> str:
        self.app_name = app_name
        self.sqs.__set_app_name__(app_name)
        self.http.__set_app_name__(app_name)

    def __sqs_execution__(self, event: Dict, context: Any) -> List[Optional[Dict]]:
        return self.sqs.process(event, context)

    def __http_execution__(self, event: Dict, context: Any) -> Dict:
        return self.http.process(event, context)

    def execute(self, event: Dict, context: Optional[Any] = None) -> Union[List[Optional[Dict]], Dict]:
        if context is None:
            context = {}
        is_sqs = event.get("Records", None)
        if is_sqs:
            return self.__sqs_execution__(event, context)
        return self.__http_execution__(event, context)

    def __set_test_mode__(self) -> None:
        self.__is_test__ = True
        self.sqs.get_sqs_client(default=SqsServiceTest)
        self.http.__set_test_mode__()
        self.sqs.__set_test_mode__()
