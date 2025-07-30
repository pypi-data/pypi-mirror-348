#  SPDX-License-Identifier: AGPL-3.0-or-later
#  Copyright (C) 2025  Dionisis Toulatos

import re
import typing
from functools import cached_property
from types import GenericAlias
from typing import Annotated, Any, Literal, Self, TypeAliasType

from pydantic import Field, PrivateAttr, conlist, model_validator

from nirahmq.enums import Category, Platform
from nirahmq.mqtt import MQTTClient, QoS, Topic
from nirahmq.utils import BaseModel, Optional, Required, Unset

type ComponentCallback[T] = typing.Callable[[T, str], None]

type StateTopic = Topic
type CommandTopic = Topic

ComponentDefaultCallback = Field(default=Unset, exclude=True)


class ComponentBase(BaseModel):
    _mqtt_client: MQTTClient = PrivateAttr()  # Make linter happy

    platform: Annotated[Platform, Required]

    # Special base topic field
    base_topic: Annotated[Optional[str], Field(serialization_alias='~')] = Unset

    ha_status_callback: Optional[ComponentCallback['ComponentBase']] = ComponentDefaultCallback

    def _abs_topic(self, topic: str) -> str:
        if self.base_topic is not Unset:
            return f"{self.base_topic}/{topic[2:]}"
        return topic

    def _is_type(self, item: Any, type_: type | TypeAliasType) -> bool:
        if item is type_:
            return True
        if isinstance(item, GenericAlias):
            for arg in item.__args__:
                if self._is_type(arg, type_):
                    return True
        if typing.get_origin(item) is Annotated:
            return self._is_type(item.__origin__, type_)
        return False

    def _has_type(self, item: Any, type_: type | TypeAliasType) -> bool:
        if item is type_:
            return True
        if isinstance(item, GenericAlias):
            for arg in item.__args__:
                if self._has_type(arg, type_):
                    return True
        if typing.get_origin(item) is Annotated:
            for metadata in item.__metadata__:
                if self._has_type(metadata, type_):
                    return True
        return False

    def publish(
            self,
            topic: Optional[str],
            payload: str | bytes | bytearray | int | float | None,
            qos: QoS = QoS.MOST,
            retain: bool = True
    ) -> None:
        if topic is Unset:
            return
        self._mqtt_client.publish(self._abs_topic(topic), payload, qos, retain)

    def _on_init(self, mqtt: MQTTClient) -> None:
        self._mqtt_client = mqtt

        # Always included fields
        for name, annotation in self.__annotations__.items():
            if self._has_type(annotation, Required):
                # Basically `self.foo = self.foo` but sets it as an explicitly set field
                setattr(self, name, getattr(self, name))

    def _on_remove(self) -> None:
        pass


class StatefulComponent(ComponentBase):
    def _on_remove(self) -> None:
        super()._on_remove()

        for topic in self._set_state_topics:
            self.publish(getattr(self, topic), None)

    @cached_property
    def _state_topics(self) -> tuple[str, ...]:
        return tuple(name for name, annot in self.__annotations__.items() if self._is_type(annot, StateTopic))

    @cached_property
    def _set_state_topics(self) -> tuple[str, ...]:
        return tuple(topic for topic in self._state_topics if topic in self.model_fields_set)


class CallableComponent(ComponentBase):
    def _on_init(self, mqtt: MQTTClient) -> None:
        super()._on_init(mqtt)

        def _callback_outer(callback_: ComponentCallback):
            def _callback_inner(payload: bytes | bytearray):
                callback_(self, payload.decode(self.encoding if isinstance(self, EntityBase) else 'utf-8'))

            return _callback_inner

        for topic, callback in self._command_mapping.items():
            topic = getattr(self, topic)
            callback = getattr(self, callback)
            self._mqtt_client.add_callback(self._abs_topic(topic), _callback_outer(callback))

    def _on_remove(self) -> None:
        super()._on_remove()

        for topic in self._command_mapping:
            topic = getattr(self, topic)
            self._mqtt_client.remove_callback(self._abs_topic(topic))
            self.publish(topic, None)

    @cached_property
    def _command_topics(self) -> tuple[str, ...]:
        return tuple(name for name, annot in self.__annotations__.items() if self._is_type(annot, CommandTopic))

    @cached_property
    def _set_command_topics(self) -> tuple[str, ...]:
        return tuple(topic for topic in self._command_topics if topic in self.model_fields_set)

    @cached_property
    def _command_mapping(self) -> dict[str, str]:
        mapping = {}
        for topic in self._set_command_topics:
            callback = re.sub(r"^(.+)_(topic)$", r"\1_callback", topic)
            if getattr(self, callback) is not Unset:
                mapping[topic] = callback
        return mapping


class AvailabilityItem(BaseModel):
    payload_available: Optional[str] = 'online'
    payload_not_available: Optional[str] = 'offline'
    topic: StateTopic
    value_template: Optional[str] = Unset


class Availability(BaseModel):
    availability: Optional[conlist(AvailabilityItem, min_length=1)] = Unset
    availability_mode: Optional[Literal['all', 'any', 'latest']] = 'latest'
    availability_template: Optional[str] = Unset
    availability_topic: Optional[StateTopic] = Unset
    payload_available: Optional[str] = 'online'
    payload_not_available: Optional[str] = 'offline'

    @model_validator(mode='after')
    def check_stuff(self) -> Self:
        if self.availability is not Unset and self.availability_topic is not Unset:
            raise ValueError('`availability_topic` and `availability` are mutually exclusive')
        return self

    def get_availability_topics(self) -> list[tuple[str, str, str]]:
        if self.availability is not Unset:
            return [(av.topic, av.payload_available, av.payload_not_available) for av in self.availability]
        if self.availability_topic is not Unset:
            return [(self.availability_topic, self.payload_available, self.payload_not_available)]
        return []


class BareEntityBase(Availability, ComponentBase):
    icon: Optional[str] = Unset
    json_attributes_template: Optional[str] = Unset
    json_attributes_topic: Optional[StateTopic] = Unset
    name: Optional[str | None] = Unset
    object_id: Optional[str] = Unset
    qos: Optional[QoS] = QoS.MOST
    unique_id: Optional[str] = Unset

    def _on_init(self, mqtt: MQTTClient) -> None:
        super()._on_init(mqtt)

        if self.availability is not Unset:
            pass

    def _on_remove(self) -> None:
        super()._on_remove()

        for topic, _, _ in self.get_availability_topics():
            self.publish(topic, None)

    def set_availability(self, state: bool) -> None:
        for topic, online, offline in self.get_availability_topics():
            self.publish(topic, online if state else offline)


class EntityBase(BareEntityBase):
    enabled_by_default: Optional[bool] = True
    encoding: Optional[str] = 'utf-8'
    entity_category: Optional[Category] = Category.NORMAL
    entity_picture: Optional[str] = Unset
