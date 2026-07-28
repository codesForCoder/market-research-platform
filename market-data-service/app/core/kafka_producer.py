import json
import ssl
from typing import Any

from aiokafka import AIOKafkaProducer
from loguru import logger

from app.core.kafka_config import KafkaConfig


class KafkaProducer:

    def __init__(self, config: KafkaConfig):

        self._config = config
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:

        if self._producer is not None:
            return

        ssl_context = ssl.create_default_context(
            cafile=self._config.ca_cert_path,
        )

        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._config.bootstrap_servers,
            security_protocol=self._config.security_protocol,
            sasl_mechanism=self._config.sasl_mechanism,
            sasl_plain_username=self._config.username,
            sasl_plain_password=self._config.password,
            ssl_context=ssl_context,
            client_id=self._config.client_id,
        )

        await self._producer.start()

        logger.info("Kafka producer started.")

    async def stop(self) -> None:

        if self._producer is None:
            return

        await self._producer.stop()

        self._producer = None

        logger.info("Kafka producer stopped.")

    async def publish(
        self,
        topic: str,
        key: str | None,
        value:  Any,
    ) -> None:

        if self._producer is None:
            raise RuntimeError("Kafka producer has not been started.")

        await self._producer.send_and_wait(
            topic=topic,
            key=key.encode() if key else None,
            value=json.dumps(value, default=str).encode("utf-8"),
        )
        logger.info("Kafka producer published {}.",json.dumps(value))