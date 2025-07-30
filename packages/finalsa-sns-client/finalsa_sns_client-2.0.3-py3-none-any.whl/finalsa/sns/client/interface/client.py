from pydantic import BaseModel
from orjson import dumps
from abc import ABC, abstractmethod
from typing import Union, Dict, List, Optional
from finalsa.traceability import (
    get_correlation_id, get_trace_id, get_span_id
)
from finalsa.traceability.functions import (
    ASYNC_CONTEXT_CORRELATION_ID,
    ASYNC_CONTEXT_TRACE_ID,
    ASYNC_CONTEXT_SPAN_ID,
)
from datetime import datetime, timezone

TOPIC_NAME = 'topic'
SUBTOPIC_NAME = 'subtopic'
PRODUCED_AT = 'produced_at'


class SnsClient(ABC):

    @abstractmethod
    def create_topic(self, name: str):
        pass

    @abstractmethod
    def subscription_exists(self, topic_name: str, arn: str) -> bool:
        pass

    @abstractmethod
    def get_all_topics(self) -> List:
        pass

    @abstractmethod
    def get_or_create_topic(self, name: str):
        pass

    @abstractmethod
    def get_topic(self, topic_name: str):
        pass

    @abstractmethod
    def list_subscriptions(self, topic: str) -> List:
        pass

    @abstractmethod
    def subscribe(self, topic_name: str, protocol: str, endpoint: str) -> Dict:
        pass

    @abstractmethod
    def publish_batch(
        self,
        topic_name: str,
        payloads: List[Dict | str], att_dict: Dict | None = ...
    ) -> Dict:
        pass

    @abstractmethod
    def publish(
        self,
        topic_name: str,
        payload: Union[Dict, str],
        att_dict: Optional[Dict] = {}
    ) -> Dict:
        pass

    @staticmethod
    def __dump_payload__(payload: Union[Dict, BaseModel, str]) -> str:
        body = None
        if isinstance(payload, str):
            return payload
        if isinstance(payload, dict):
            body = dumps(payload)
            return body.decode()
        body = payload.model_dump_json()
        return body

    @staticmethod
    def __dump_batch_payload__(payload_list: List[Union[Dict, BaseModel]], attrs:  Dict | None = ...) -> List[Dict[str, str]]:
        result = []
        for payload in payload_list:
            body = SnsClient.__dump_payload__(payload)
            result.append({
                'Message': body,
                'MessageAttributes': attrs
            })
        return result

    @staticmethod
    def __parse_to_message__(
        payload: Union[Dict, BaseModel],
    ) -> Dict:
        if isinstance(payload, BaseModel):
            return payload.model_dump()
        return payload

    def get_default_attrs(
        self,
        topic: Optional[str] = None,
        subtopic: Optional[str] = None,
    ) -> Dict:
        result = {
            ASYNC_CONTEXT_CORRELATION_ID: get_correlation_id(),
            ASYNC_CONTEXT_TRACE_ID: get_span_id(),
            ASYNC_CONTEXT_SPAN_ID: get_trace_id(),
            PRODUCED_AT: datetime.now(timezone.utc).isoformat(),
        }
        if topic:
            result[TOPIC_NAME] = topic
        if subtopic:
            result[SUBTOPIC_NAME] = subtopic
        return result

    def publish_message(
        self,
        topic_name: str,
        payload: Union[Dict, BaseModel],
        subtopic: Optional[str] = None,
    ) -> Dict:
        message_attrs = self.get_default_attrs(topic_name, subtopic)
        message = self.__parse_to_message__(payload)
        return self.publish(topic_name, message, message_attrs)

    def publish_messages_batch(
        self,
        topic_name: str,
        payloads: List[Dict | str],
        subtopic: Optional[str] = None,
    ) -> Dict:
        message_attrs = self.get_default_attrs(topic_name, subtopic)
        return self.publish_batch(topic_name, payloads, message_attrs)
