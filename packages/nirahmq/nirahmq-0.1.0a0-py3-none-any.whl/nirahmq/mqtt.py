#  SPDX-License-Identifier: AGPL-3.0-or-later
#  Copyright (C) 2025  Dionisis Toulatos

import time
from enum import IntEnum
from queue import SimpleQueue
from typing import Annotated, Any, Callable, Self

import paho.mqtt as pmq
from paho.mqtt import client as pmq_client
from paho.mqtt.subscribeoptions import SubscribeOptions
from pydantic import Field

type Topic = Annotated[str, Field(pattern=r"^(?:(?:~/)?[a-zA-Z0-9_-]+)(?:/[a-zA-Z0-9_-]+)*$")]


def check_mqtt_error(func: Callable[[...], pmq.enums.MQTTErrorCode], *args, **kwargs) -> None:
    if (err := func(*args, **kwargs)) != pmq.enums.MQTTErrorCode.MQTT_ERR_SUCCESS:
        raise RuntimeError(f"Failed to call function {func.__name__}: {err}")


class QoS(IntEnum):
    MOST = 0  # At most once
    LEAST = 1  # At least once
    EXACTLY = 2  # Exactly once


class MQTTClient:
    _mqtt_client: pmq_client.Client
    _mqtt_queue: SimpleQueue

    _hostname: str
    _port: int
    _client_id: str

    _subscriptions: SimpleQueue[str]

    def __init__(
            self,
            hostname: str,
            port: int = 1883,
            username: str | None = None,
            password: str | None = None,
            client_id: str = "nirahmq"
    ):
        self._hostname = hostname
        self._port = port
        self._client_id = client_id

        self._mqtt_client = pmq_client.Client(
            pmq.enums.CallbackAPIVersion.VERSION2,
            client_id,
            protocol=pmq_client.MQTTv5
        )

        if username is not None:
            self._mqtt_client.username_pw_set(username, password)

        self._mqtt_client.on_connect = self._on_connect
        self._mqtt_client.on_connect_fail = self._on_connect_fail
        self._mqtt_client.on_disconnect = self._on_disconnect

        self._mqtt_queue = SimpleQueue()

        self._subscriptions = SimpleQueue()

    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def port(self) -> int:
        return self._port

    @property
    def client_id(self) -> str:
        return self._client_id

    def _on_connect(
            self,
            client: pmq_client.Client,
            userdata: Any,
            flags: dict[str, Any],
            reason: pmq.reasoncodes.ReasonCode,
            properties: pmq.properties.Properties | None
    ) -> None:
        if not self._subscriptions.empty():
            opts = SubscribeOptions()
            topics = []
            while not self._subscriptions.empty():
                topics.append((self._subscriptions.get(), opts))
            self._mqtt_client.subscribe(topics)
        self._mqtt_queue.put(True)

    def _on_connect_fail(
            self,
            client: pmq_client.Client,
            userdata: Any
    ) -> None:
        self._mqtt_queue.put(False)

    def _on_disconnect(
            self,
            client: pmq_client.Client,
            userdata: Any,
            reason: pmq.reasoncodes.ReasonCode,
            properties: pmq.properties.Properties | None
    ) -> None:
        pass  # TODO: Handle gracefully

    # TODO: This thing acts weird. Needs more investigating
    def set_will(self, topic: str, payload: str) -> None:  # NOTE: Must be called before `connect`
        self._mqtt_client.will_set(topic, payload)

    def add_callback(self, topic: str, callback: Callable[[bytes | bytearray], None]) -> None:
        self._mqtt_client.message_callback_add(topic, lambda c, u, m: callback(m.payload))
        if self._mqtt_client.is_connected():
            self._mqtt_client.subscribe((topic, SubscribeOptions()))
        else:
            self._subscriptions.put(topic)

    def remove_callback(self, topic: str) -> None:
        if self._mqtt_client.is_connected():
            # TODO: Needs more testing. Is it safe immediately return after `message_callback_remove`
            self._mqtt_client.message_callback_remove(topic)
            self._mqtt_client.unsubscribe(topic)

    def connect(self) -> bool:
        if not self._mqtt_client.is_connected():
            check_mqtt_error(self._mqtt_client.connect, self._hostname, self._port)
            self._mqtt_client.loop_start()
            return self._mqtt_queue.get()
        return False

    def disconnect(self) -> None:
        if self._mqtt_client.is_connected():
            while self._mqtt_client.want_write():
                time.sleep(0.01)
            check_mqtt_error(self._mqtt_client.disconnect)

    def publish(
            self,
            topic: str,
            payload: str | bytes | bytearray | int | float | None,
            qos: QoS = QoS.MOST,
            retain: bool = True
    ) -> None:
        if self._mqtt_client.is_connected():
            self._mqtt_client.publish(topic, payload, int(qos), retain)
