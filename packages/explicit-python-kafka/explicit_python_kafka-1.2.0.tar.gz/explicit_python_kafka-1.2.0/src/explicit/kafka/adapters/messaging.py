"""Реализация адаптера обмена сообщениями."""
from typing import Dict
from typing import Generator
from typing import Optional
import logging

from confluent_kafka import Consumer as Subscriber
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from confluent_kafka import Message as KafkaMessage
from confluent_kafka import Producer as Publisher
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

from explicit.adapters.messaging import AbstractAdapter
from explicit.kafka.domain.model import PublishConfig
from explicit.kafka.domain.model import SubscribeConfig


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def publish_callback(error, message: KafkaMessage):
    if error is not None:
        logger.error('Ошибка при публикации сообщения: %s', error)
    else:
        logger.info('Сообщение доставлено: %s [%s]', message.topic(), message.partition())
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Тело сообщения: %s', message.value())


class Adapter(AbstractAdapter):

    """Адаптер обмена сообщениями через Kafka."""

    def __init__(
        self, *,
        subscribe_config: Optional[SubscribeConfig] = None,
        publish_config: Optional[PublishConfig] = None,
        must_ensure_topics: Optional[bool] = True
    ) -> None:
        """Инициализация адаптера.

        :param subscribe_config: параметры роли подписчика.
        :param publish_config: параметры роли издателя.
        :param must_ensure_topics: убедиться в существовании топика
            перед выполнением действий.
        """
        self._subscribe_config = subscribe_config
        self._publish_config = publish_config
        self._publisher: Publisher = None
        self._subscribers: Dict[str, Subscriber] = {}
        self._must_ensure_topics = must_ensure_topics

        self._available_config = self._publish_config or self._subscribe_config

    def _ensure_topics(self, *topics: str):
        existing_topics = self.list_topics()

        new_topics = [topic for topic in topics if topic not in existing_topics]

        if not new_topics:  # Все используемые топики созданы
            return

        self.create_topics(*new_topics)

    def _ensure_publisher(self):
        if self._publish_config is None:
            raise RuntimeError('Publisher is not configured')

        if self._publisher is None:
            self._publisher = Publisher(self._publish_config.dict(by_alias=True))

        return self._publisher

    def _make_subscriber_key(self, *topics: str) -> str:
        return ','.join(sorted(topics))

    def _ensure_subscriber(self, *topics: str) -> Subscriber:
        if self._subscribe_config is None:
            raise RuntimeError('Subscriber is not configured')

        key = self._make_subscriber_key(*topics)

        subscriber = self._subscribers.get(key)

        if subscriber is None:
            self._subscribers[key] = Subscriber(self._subscribe_config.dict(by_alias=True))
        return self._subscribers[key]

    def _should_continue_polling(
        self, message: KafkaMessage, break_on_eof: bool, break_on_error: bool
    ) -> Optional[bool]:
        """Продолжать ли опрос, если возникла ошибка или был достигнут конец партиции.

        :param message: Сообщение из Kafka.
        :param break_on_eof: Останавливать опрос подписчика при исчерпании сообщений.
        :param break_on_error: Останавливать опрос подписчика при ошибках.
        :return: True если нужно продолжить опрос, False нужно прекратить опрос, None действия не требуются.
        """
        eof = message is None or message.error() == KafkaError._PARTITION_EOF  # pylint: disable=protected-access
        if eof:
            return not break_on_eof
        elif error := message.error():
            logger.error('Ошибка при получении сообщения: %s', error)
            return not break_on_error
        return None

    def _poll_subscriber(
        self,
        subscriber: Subscriber,
        break_on_eof: bool = False,
        break_on_error: bool = False,
    ) -> Generator[KafkaMessage, None, None]:
        """Опрашивает подписчики и генерирует сообщения.

        :param subscriber: Набор подписчиков для опроса.
        :param break_on_eof: Останавливать опрос подписчика при исчерпании сообщений.
        :param break_on_error: Останавливать опрос подписчика при ошибках.
        :return: Генератор сообщений из Kafka.
        """

        while True:
            message: KafkaMessage = subscriber.poll(1.0)

            continue_polling = self._should_continue_polling(message, break_on_eof, break_on_error)
            if continue_polling is True:
                continue
            elif continue_polling is False:
                break

            logger.info('Получено сообщение из %s', message.topic())
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Тело сообщения: %s', message.value())

            yield message

    def publish(self, topic: str, message: str, *args, **kwargs) -> None:  # pylint: disable=unused-argument
        publisher = self._ensure_publisher()

        if self._must_ensure_topics:
            self._ensure_topics(topic)

        publisher.poll(0)
        publisher.produce(topic, message, callback=publish_callback)
        publisher.flush()

    def subscribe(self, *topics: str) -> Generator[KafkaMessage, None, None]:
        subscriber: Subscriber = self._ensure_subscriber(*topics)

        if self._must_ensure_topics:
            self._ensure_topics(*topics)

        subscriber.subscribe(list(topics))

        yield from self._poll_subscriber(subscriber)

    def commit(self, message: KafkaMessage, *topics: str):
        subscriber: Subscriber = self._ensure_subscriber(*topics)
        subscriber.commit(message)

    def list_topics(self, timeout=30.0):
        admin = self._get_admin_client()
        return list(admin.list_topics(timeout=timeout).topics.keys())

    def create_topics(self, *topics: str, timeout=30.0):
        admin = self._get_admin_client()
        futures = admin.create_topics(
            [
                NewTopic(topic, num_partitions=1) for topic in topics
            ],
            request_timeout=timeout
        )

        for topic, future in futures.items():
            try:
                future.result()
            except KafkaException as e:
                error = e.args[0]
                if error.code() in ('TOPIC_ALREADY_EXISTS', ):
                    logger.warning('Топик уже существует')

            except Exception:  # pylint: disable=broad-exception-caught
                logger.exception('Невозможно создать topic')

            else:
                logger.info('Topic %s создан', topic)

    def delete_topic(self, topic: str):
        """Удалить единичный топик."""
        return self.delete_topics(topic)[0]

    def delete_topics(self, *topics: str):
        """Удалить набор топиков."""
        admin = self._get_admin_client()
        return [
            (topic, future.result())
            for topic, future in admin.delete_topics(list(topics)).items()
        ]

    def _get_admin_client(self):
        if self._available_config is None:
            raise RuntimeError('Не указаны параметры подключения')

        return AdminClient(self._available_config.dict(by_alias=True))
