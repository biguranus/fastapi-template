# -*- coding:utf-8 -*-
import sys
import json
import time

from mq_http_sdk.mq_client import MQClient
from mq_http_sdk.mq_producer import TopicMessage, MQExceptionBase

from src.libs.logging import logger
from src.config import (
    ALIYUN_ACCESS_KEY_ID,
    ALIYUN_ACCESS_KEY_SECRET,
    MQ_HTTP_ENDPOINT,
    MQ_INSTANCE_ID,
    MQ_TOPIC_NAME,
    MQ_GROUP_ID,
    MQ_BATCH,
    MQ_WAIT_SECONDS,
)


def get_mq_client():
    return MQClient(
        host=MQ_HTTP_ENDPOINT,
        access_id=ALIYUN_ACCESS_KEY_ID,
        access_key=ALIYUN_ACCESS_KEY_SECRET,
    )


mq_client = get_mq_client()


class RocketmqService:
    def __init__(self, topic=MQ_TOPIC_NAME, group_id=MQ_GROUP_ID, batch=MQ_BATCH):
        self.topic = topic
        self.group_id = group_id
        self.batch = batch
        self.wait_seconds = MQ_WAIT_SECONDS
        self.instance_id = MQ_INSTANCE_ID

    def send_message(self, msg, delay=False, delay_time_in_millis=0, tag=""):
        producer = mq_client.get_producer(
            instance_id=self.instance_id, topic_name=self.topic
        )
        try:
            message = TopicMessage(message_body=msg, message_tag=tag)
            if delay:
                message.set_start_deliver_time(
                    int(round(time.time() * 1000)) + delay_time_in_millis
                )
            result = producer.publish_message(message)
            logger.debug(f"Publish Mesaage succeed. MessageID: {result.message_id}")
        except MQExceptionBase as e:
            if e.type == "TopicNotExist":
                logger.error("Topic not exist, please create it.")
                sys.exit(1)
            logger.error(f"Publish Message Fail. Exception: {e}")

    def consume_message(self, handler):
        consumer = mq_client.get_consumer(
            instance_id=self.instance_id, topic_name=self.topic, consumer=self.group_id
        )
        while True:
            try:
                recv_msgs = consumer.consume_message(self.batch, self.wait_seconds)
                for msg in recv_msgs:
                    body = json.loads(msg.message_body)
                    logger.debug(f"Receive message_id: {msg.message_id}, body: {body}")
                    try:
                        handler(body)
                    except Exception as e:
                        logger.error(f"处理消息出错 exception: {e}")
                        continue
                    else:
                        try:
                            consumer.ack_message([msg.receipt_handle])
                            logger.debug(
                                f"AK message_id: {msg.message_id} Message succeed."
                            )
                        except MQExceptionBase as e:
                            logger.error(f"AK message fail. Exception: {e}")
                            if e.sub_errors:
                                for sub_error in e.sub_errors:
                                    logger.error(
                                        f"ErrorHandle: {sub_error['ReceiptHandle']}, ErrorCode:{sub_error['ErrorCode']},"  # noqa
                                        f"ErrorMsg:{sub_error['ErrorMessage']}"
                                    )
                            continue
            except MQExceptionBase as e:
                if e.type == "MessageNotExist":
                    logger.info(f"No new message! RequestId: {e.req_id}")
                    continue
                logger.error(f"Consume Message Fail! Exception: {e}")
                time.sleep(2)
                continue


rocketmq_service = RocketmqService()
