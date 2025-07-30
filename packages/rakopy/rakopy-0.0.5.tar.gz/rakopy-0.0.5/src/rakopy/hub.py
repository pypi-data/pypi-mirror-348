"""Core implementation of rakopi module."""
from __future__ import annotations

import logging

import asyncio
import json
from typing import Any, AsyncGenerator, List
from rakopy.consts import DEFAULT_PORT
from rakopy.errors import ConfigValidationError, SendCommandError
from rakopy.model import (
    Channel,
    ChannelLevel,
    HubStatus,
    Level,
    LevelChangedEvent,
    LevelInfo,
    Room,
    Scene,
    SceneChangedEvent
)

_LOGGER = logging.getLogger(__name__)


class Hub:
    """Class to integrate with Rako Hub."""
    def __init__(
        self,
        client_name: str,
        host: str,
        port: int = DEFAULT_PORT
    ):
        host = host.strip()
        if not host:
            raise ConfigValidationError("RakoHub: host parameter cannot be empty.")

        if port < 0 or port > 65535:
            raise ConfigValidationError("RakoHub: port should be between 0 and 65535.")

        if not client_name:
            raise ConfigValidationError("RakoHub: client_name parameter cannot be empty.")

        self.host = host
        self.port = port
        self.client_name = client_name

        self._lock = asyncio.Lock()
        self._reader = None
        self._writer = None

    async def get_hub_status(self) -> HubStatus:
        """
        Get Rako Hub status.
        """
        await self._reconnect()

        request = {
            "name": "status",
            "payload": {}
        }

        self._writer.write(str.encode(json.dumps(request) + "\r\n"))
        await self._writer.drain()

        response = await self._reader.readline()
        json_data = json.loads(response)

        return HubStatus(
            product_type = json_data["payload"]["productType"],
            protocol_version = int(json_data["payload"]["protocolVersion"]),
            id = json_data["payload"]["hubId"],
            mac_address = json_data["payload"]["mac;"],
            version = json_data["payload"]["hubVersion"]
        )

    async def get_levels(self, room_id: int = None) -> List[Level]:
        """
        Get levels for all the channels in a room.
        If room_id is not specified, returns levels for all the rooms.
        """
        return await self._query("LEVEL", self._to_level, room_id)

    async def get_rooms(self, room_id: int = None) -> List[Room]:
        """
        Get room by its id.
        If room_id is not specified, returns all rooms.
        """
        return await self._query("SCENECHANNEL", self._to_room, room_id)

    async def set_level(self, room_id: int, channel_id: int, level: int) -> None:
        """
        Set level for a given room and channel.
        """
        action = {
            "command": "levelrate",
            "level": level
        }

        request = self._build_send_request(room_id, channel_id, action)

        await self._send(request)

    async def set_rgb(
            self,
            room_id: int,
            channel_id: int,
            red: int,
            green: int,
            blue: int,
            rgb_excludes_brightness: bool = False,
            level: int = None
        ) -> None:
        """
        Set RGB for a given room and channel.
        """
        color_send_type = "SEND_COLOR_AND_LEVEL"
        if rgb_excludes_brightness and not level:
            color_send_type = "SEND_COLOR_ONLY"

        request = {
            "name": "send-color",
            "payload": {
                "room": room_id,
                "channel": channel_id,
                "colorSendType": color_send_type,
                "red": red,
                "green": green,
                "blue": blue,
                "rgbExcludesBrightness": rgb_excludes_brightness,
                "level": level
            }
        }

        await self._send(request)

    async def set_scene(self, room_id: int, channel_id: int, scene: int) -> None:
        """
        Set a scene for a given room and channel.
        """
        action = {
            "command": "scene",
            "scene": scene
        }

        request = self._build_send_request(room_id, channel_id, action)

        await self._send(request)

    async def set_temperature(
            self,
            room_id: int,
            channel_id: int,
            temperature: int,
            level: int = None
        ) -> None:
        """
        Set a colour temperature and level for a given room and channel.
        """
        color_send_type = "SEND_COLOR_ONLY"
        if level:
            color_send_type = "SEND_COLOR_AND_LEVEL"

        request = {
            "name": "send-colorTemp",
            "payload": {
                "room": room_id,
                "channel": channel_id,
                "colorSendType": color_send_type,
                "temperature": temperature,
                "level": level
            }
        }

        await self._send(request)

    async def start_fading_down(self, room_id: int, channel_id: int) -> None:
        """
        Start fading down brightness for a given room and channel
        """
        action = {
            "command": "fade",
            "down": True
        }

        request = self._build_send_request(room_id, channel_id, action)

        await self._send(request)

    async def start_fading_up(self, room_id: int, channel_id: int) -> None:
        """
        Start fading up brightness for a given room and channel.
        """
        action = {
            "command": "fade",
            "down": False
        }

        request = self._build_send_request(room_id, channel_id, action)

        await self._send(request)

    async def stop_fading(self, room_id: int, channel_id: int) -> None:
        """
        Stop fading brightness for a given room and channel
        """
        action = {
            "command": "stop"
        }

        request = self._build_send_request(room_id, channel_id, action)

        await self._send(request)

    async def store_scene(self, room_id: int, channel_id: int, scene: int) -> None:
        """
        Store current levels as a scene for a given room and channel.
        """
        action = {
            "command": "store",
            "scene": scene
        }

        request = self._build_send_request(room_id, channel_id, action)

        await self._send(request)

    async def get_events(self) -> AsyncGenerator:
        """
        Subscribe and listen to events from Hub asynchronously.
        """
        reader: asyncio.StreamReader = None
        writer: asyncio.StreamWriter = None

        while True:
            if (writer is None or
                writer.transport is None or
                writer.transport.is_closing()
            ):
                reader, writer = await asyncio.open_connection(self.host, self.port)

            payload = {
                "version": 2,
                "client_name": self.client_name,
                "subscriptions": ["TRACKER"]
            }
            request = f"SUB,JSON,{json.dumps(payload)}\r\n"

            writer.write(str.encode(request))
            await writer.drain()

            try:
                while True:
                    response = await reader.readline()
                    json_data = json.loads(response)
                    if json_data["name"] == "tracker":
                        if json_data["type"] == "scene":
                            yield SceneChangedEvent(
                                room_id = json_data["payload"]["roomId"],
                                channel_id = json_data["payload"]["channelId"],
                                scene_id = json_data["payload"]["scene"],
                                active_scene_id = json_data["payload"]["activeScene"],
                            )
                        elif json_data["type"] == "level":
                            level_changed_event = LevelChangedEvent(
                                room_id = json_data["payload"]["roomId"],
                                channel_id = json_data["payload"]["channelId"],
                                current_level = json_data["payload"]["currentLevel"],
                                target_level = json_data["payload"]["targetLevel"],
                                time_to_take = json_data["payload"]["timeToTake"],
                                temporary = json_data["payload"]["temporary"],
                            )
                            yield level_changed_event
            except ConnectionError as e:
                _LOGGER.exception("Unexpected exception: %s", repr(e))

    async def _query(self, query_type: str, func, room_id: int = None):
        """
        Executes query and returns result.
        """
        await self._reconnect()

        await self._lock.acquire()
        try:
            if room_id is None:
                room_id = 0

            request = {
                "name": "query",
                "payload": {
                    "queryType": query_type,
                    "roomId": room_id
                }
            }

            self._writer.write(str.encode(json.dumps(request) + "\r\n"))
            await self._writer.drain()

            response = (await self._reader.readline()).decode()
            json_data = json.loads(response)

            result = []
            for data in json_data["payload"]:
                result.append(func(data))

            return result
        finally:
            self._lock.release()

    async def _reconnect(self) -> None:
        """
        Try to reconnect to the Rako Hub if the connection was not previously
        established or was closed.
        """
        await self._lock.acquire()
        try:
            if (self._writer is None or
                self._writer.transport is None or
                self._writer.transport.is_closing()
            ):
                self._reader, self._writer = await asyncio.open_connection(self.host, self.port)

                payload = {
                    "version": 2,
                    "client_name": self.client_name,
                    "subscriptions": []
                }
                request = f"SUB,JSON,{json.dumps(payload)}\r\n"

                self._writer.write(str.encode(request))
                await self._writer.drain()

                await self._reader.readline()
        finally:
            self._lock.release()

    async def _send(self, request: Any) -> None:
        """
        Sends a command.
        """
        await self._reconnect()

        await self._lock.acquire()
        try:
            self._writer.write(str.encode(json.dumps(request) + "\r\n"))
            await self._writer.drain()

            response = (await self._reader.readline()).decode()
            json_data = json.loads(response)
            if json_data["name"] == "error":
                raise SendCommandError(
                    f"Failed to send {0} command. Error: {1}", request, json_data["payload"]
                )
        finally:
            self._lock.release()

    @staticmethod
    def _build_send_request(room_id: int, channel_id: int, action: Any):
        """
        Returns a send command request.
        """
        return {
            "name": "send",
            "payload": {
                "room": room_id,
                "channel": channel_id,
                "action": action
            }
        }

    @staticmethod
    def _to_level(data: Any) -> Level:
        """
        Converts list of str to Level.
        """
        channel_levels = []
        for channel_level in data["channel"]:
            level_info_data = channel_level["levelInfo"]
            if level_info_data:
                level_info = LevelInfo(
                    kelvin = level_info_data["kelvin"],
                    red = level_info_data["red"],
                    green = level_info_data["green"],
                    blue = level_info_data["blue"]
                )
            else:
                level_info = None

            channel_levels.append(
                ChannelLevel(
                    channel_id = channel_level["channelId"],
                    current_level = channel_level["currentLevel"],
                    target_level = channel_level["targetLevel"],
                    level_info = level_info
                )
            )

        return Level(
            room_id = data["roomId"],
            current_scene_id = data["currentScene"],
            channel_levels = channel_levels
        )

    @staticmethod
    def _to_room(data: Any) -> Room:
        """
        Converts JSON data to Room.
        """
        channels = []
        channel_1 = True
        color_type_1 = None
        color_title_1 = None
        multi_channel_component_1 = None
        for channel in data["channel"]:
            if channel_1:
                channel_1 = False
                color_type_1 = channel.get("colorType", None)
                color_title_1 = channel.get("colorTitle", None)
                multi_channel_component_1 = channel.get("multiChannelComponent", None)

            channels.append(
                Channel(
                    id = channel["channelId"],
                    title = channel["title"],
                    type = channel["type"],
                    color_type = channel.get("colorType", color_type_1),
                    color_title = channel.get("colorTitle", color_title_1),
                    multi_channel_component = channel.get(
                        "multiChannelComponent", multi_channel_component_1)
                )
            )

        scenes = []
        scenes.append(
            Scene(
                id = 0,
                title = "Off"
            )
        )

        for scene in data["scene"]:
            scenes.append(
                Scene(
                    id = scene["sceneId"],
                    title = scene["title"]
                )
            )

        return Room(
            id = data["roomId"],
            title = data["title"],
            type = data["type"],
            mode = data.get("mode", None),
            channels = channels,
            scenes = scenes
        )
