from finalsa.common.lambdas.sqs.get_handler_filled_args import get_handler_filled_args
from typing import Callable, Optional, Union, Dict, Any, List, Tuple
from finalsa.common.lambdas.common.constants import TIMESTAMP_HEADER
from finalsa.common.lambdas.common.AppHandler import AppHandler
from finalsa.common.lambdas.sqs.SqsEvent import SqsEvent
from finalsa.sqs.client import SqsService, SqsServiceImpl
from finalsa.traceability.functions import (
    ASYNC_CONTEXT_CORRELATION_ID,
    ASYNC_CONTEXT_TRACE_ID,
)
from finalsa.common.models import AsyncMeta
from finalsa.traceability import (
    default_span_id,
    default_trace_id,
    set_correlation_id,
    set_span_id,
    set_trace_id,
    get_correlation_id
)
from datetime import datetime, timezone
from logging import Logger
from time import time


class SqsHandler(AppHandler):
    def __init__(
        self,
        app_name: str = None,
        logger: Logger = None,
        test_mode: Optional[bool] = False
    ) -> None:
        super().__init__(app_name, logger, test_mode)
        self.handlers = {}
        self.handlers_args = {}
        self.retries = {}
        self.sqs_client = None
        self.sqs_urls_cache = {}

    def get_sqs_client(self, default=SqsServiceImpl) -> SqsService:
        if self.sqs_client is None:
            self.sqs_client = default()
        return self.sqs_client

    def __get_handler__(self, topic: str) -> Optional[Callable[[Union[Dict, SqsEvent]], Union[Dict, str]]]:
        if topic not in self.handlers:
            return self.handlers.get("default")
        return self.handlers.get(topic)

    def __get_retries__(self, topic: str) -> int:
        if topic not in self.retries:
            return self.retries.get("default", 0)
        return self.retries.get(topic)

    def __try_excecution_str__(
        self,
        message: SqsEvent,
        meta: AsyncMeta,
    ) -> Tuple[Optional[Union[Dict, str]], bool]:
        try:
            handler = self.__get_handler__("default")
            handler_attrs = self.handlers_args["default"]
            filled_args = get_handler_filled_args(
                handler_attrs, {}, message, meta)
            response = handler(**filled_args)
            return response, True
        except Exception as e:
            self.logger.error("Error processing sqs event", extra={
                "error": e,
            })
            return None, False

    def __try_excecution_dict__(
            self,
            payload: Dict,
            message: SqsEvent,
            meta : AsyncMeta,
            handler: Optional[Callable] = None,
            retries: Optional[int] = None
    ) -> Tuple[Optional[Union[Dict, str]], bool]:
        topic = message.topic
        if topic not in self.handlers:
            topic = "default"
        if retries is None:
            retries = self.__get_retries__(topic)
        if handler is None:
            handler = self.__get_handler__(topic)
        try:
            handler = self.__get_handler__(topic)
            handler_attrs = self.handlers_args[topic]
            filled_args = get_handler_filled_args(
                handler_attrs, payload, message, meta)
            response = handler(**filled_args)
            return response, True
        except Exception as e:
            if retries > 0:
                self.logger.error("Error processing sqs event", extra={
                    "error": e,
                    "retries": retries
                })
                return self.__try_excecution_dict__(payload, message, meta, handler, retries - 1)
            else:
                self.logger.error("Error processing sqs event", extra={
                    "error": e,
                    "retries": retries
                })
                return None, False

    def __set_context_and_get_meta__(self, message: SqsEvent) -> AsyncMeta:
        correlation = message.message_attributes.get(
            ASYNC_CONTEXT_CORRELATION_ID,
            None
        )
        set_correlation_id(correlation, self.app_name)
        trace_id = message.message_attributes.get(
            ASYNC_CONTEXT_TRACE_ID,
            default_trace_id()
        )
        set_trace_id(trace_id)
        timestamp = message.message_attributes.get(
            TIMESTAMP_HEADER,
            None
        )
        if self.__is_test__ and timestamp is not None:
            timestamp = datetime.fromisoformat(timestamp)
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        if not timestamp or isinstance(timestamp, str):
            timestamp = datetime.now(timezone.utc)
        return AsyncMeta(
            correlation_id=get_correlation_id(),
            timestamp=timestamp,
            topic=message.topic,
        )

    def __try_excution__(
        self,
        message: SqsEvent
    ) -> Tuple[Optional[Union[Dict, str]], bool]:
        content = message.get_payload()
        meta = self.__set_context_and_get_meta__(message)
        if isinstance(content, dict):
            return self.__try_excecution_dict__(content, message, meta)
        if isinstance(content, str):
            return self.__try_excecution_str__(message, meta)
        return None, False

    def __get_sqs_url__(self, sqs_name: str) -> str:
        if sqs_name in self.sqs_urls_cache:
            return self.sqs_urls_cache[sqs_name]
        sqs_url = self.get_sqs_client().get_queue_url(sqs_name)
        self.sqs_urls_cache[sqs_name] = sqs_url
        return sqs_url

    def __delete_message__(self, message: SqsEvent) -> None:
        sqs_arn = message.event_source_arn
        receipt_handle = message.receipt_handle
        sqs_name = sqs_arn.split(":")[-1]
        sqs_url = self.__get_sqs_url__(sqs_name)
        self.get_sqs_client().delete_message(sqs_url, receipt_handle)

    def process(self, event: Dict, context: Any) -> List[Dict]:
        if context is not None and hasattr(context, "aws_request_id"):
            set_span_id(context.aws_request_id)
        else:
            set_span_id(default_span_id())
        records = event['Records']
        responses = []
        for record in records:
            message = SqsEvent.from_sqs_lambda_event(record)
            response, is_sucess = self.__try_excution__(message)
            if is_sucess:
                self.__delete_message__(message)
            responses.append(response)
        return responses

    def handler(self, topic: str, retries: Optional[int] = 0) -> Callable:
        if retries < 0:
            raise ValueError("Retries must be greater or equal than 0")
        if topic in self.handlers:
            raise ValueError("Topic already has a handler")
        self.retries[topic] = retries

        def decorator(handler: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Optional[Union[Dict, str]]:
                self.logger.info("Processing sqs event", extra={
                    "topic": topic,
                    "retries": retries
                })
                start = time()
                result = handler(*args, **kwargs)
                end = time()
                self.logger.info("Processed sqs event", extra={
                    "result": result,
                    "topic": topic,
                    "retries": retries,
                    "duration": end - start
                })
                return result
            self.handlers_args[topic] = handler.__annotations__
            self.handlers[topic] = wrapper
            return wrapper
        return decorator

    def default(self, retries: Optional[int] = 1) -> Callable:
        return self.handler("default", retries)

    def __merge__(self, other: 'SqsHandler') -> None:
        for topic, handler in other.handlers.items():
            if topic in self.handlers:
                raise ValueError("Topic already has a handler")
            self.handlers[topic] = handler
            self.handlers_args[topic] = other.handlers_args[topic]
        for topic, retries in other.retries.items():
            if topic in self.retries:
                raise ValueError("Topic already has a handler")
            self.retries[topic] = retries
