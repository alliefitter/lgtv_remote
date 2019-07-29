from abc import ABC, abstractmethod
from typing import NamedTuple

from yaml import safe_load, safe_dump


class TvSettings(NamedTuple):
    host: str
    client_key: str


class SettingsInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> TvSettings:
        raise NotImplementedError

    @abstractmethod
    def load(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def serialize(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, host: str, client_key: str):
        raise NotImplementedError


class Settings(SettingsInterface):
    def __init__(self):
        self._settings = {}

    def get(self, key: str) -> TvSettings:
        return TvSettings(**self._settings.get(key))

    def load(self, path: str):
        with open(path, 'r') as file_object:
            self._settings = safe_load(file_object)

    def serialize(self, path: str):
        with open(path, 'w') as file_object:
            safe_dump(self._settings, file_object)

    def set(self, key: str, host: str, client_key: str):
        self._settings[key] = {'host': host, 'client_key': client_key}
