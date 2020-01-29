from django.apps import AppConfig


class SocketConsumerConfig(AppConfig):
    name = 'socket_consumer'
    verbose_name = 'An app which consumes the data provided by the websocket of the VRI ESB'
