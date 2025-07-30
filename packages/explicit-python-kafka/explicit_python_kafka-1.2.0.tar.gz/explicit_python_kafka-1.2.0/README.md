# Explicit-Kafka
## Набор компонентов для интеграции explicit с kafka.

Содержит реализацию адаптера обмена сообщениями через Kafka.

### Пример использования
Настройка адаптера
```python
# persons/core/apps.py
from django.apps.config import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):

    name = __package__
    
    def _setup_adapter(self):
        from explicit.kafka.adapters.messaging import Adapter
        from explicit.kafka.adapters.messaging import PublishConfig
        from explicit.kafka.adapters.messaging import SubscribeConfig

        from persons import core
        
        # конфигурация адаптера
        adapter_base_config = {'bootstrap.servers': 'kafka:9092'}
        publish_config = PublishConfig(adapter_base_config)
        subscribe_config = SubscribeConfig(adapter_base_config | {'group.id': f'edu.persons'})
    
        adapter = Adapter(subscribe_config=subscribe_config, publish_config=publish_config)
        core.adapter = adapter

    def ready(self):
        self._setup_adapter()
```
Отправка сообщений
```python
# persons/core/persons/services/handlers/events.py

def on_person_created(
    event: 'PersonCreated',
    messaging_adapter: 'AbstractMessagingAdapter'
):
    messaging_adapter.publish('edu.persons.person', event.dump())
```

Подписка на сообщения
```python
# education/entrypoints/eventconsumer.py

def bootstrap():
    import json
    
    from education.core import adapter
    from education.core import bus
    from education.core.persons.domain.events import PersonCreated 
    
    TOPIC_EVENTS = {
      'edu.persons.person': PersonCreated,
    }
    
    for message in adapter.subscribe(*TOPIC_EVENTS):
       for message in adapter.subscribe(*TOPIC_EVENTS):
          event = TOPIC_EVENTS[message.topic()](
              **json.loads(message.value())
          )
          bus.handle(event)

bootstrap()
```

### Запуск тестов
```sh
$ tox
```
