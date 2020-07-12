from abc import ABC, abstractmethod
from argparse import Namespace, ArgumentParser
from typing import Optional, Dict, Tuple, List, Type

from pywebostv.controls import WebOSControlBase

from lgtv_remote.adapter import WebOSClientAdapter


class CommandMetaInterface(ABC):
    @property
    @abstractmethod
    def help(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError


class CommandInterface(CommandMetaInterface, ABC):
    @property
    @abstractmethod
    def defaults(self) -> Dict:
        raise NotImplementedError

    @property
    @abstractmethod
    def options(self) -> Tuple[Dict, ...]:
        raise NotImplementedError

    @abstractmethod
    def execute(self, namespace: Namespace):
        raise NotImplementedError


class CommandGroupInterface(CommandMetaInterface, ABC):
    @property
    @abstractmethod
    def metavar(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def subcommands(self) -> Tuple[CommandMetaInterface, ...]:
        raise NotImplementedError

    @abstractmethod
    def get_parents(self, base_parser: ArgumentParser) -> List[ArgumentParser]:
        raise NotImplementedError


class CommandBase(CommandInterface, ABC):
    @property
    def defaults(self) -> Dict:
        return {}


class CommandGroupBase(CommandGroupInterface, ABC):
    def __init__(self, subcommands: Tuple[CommandMetaInterface, ...]):
        self._subcommands = subcommands

    @property
    def subcommands(self) -> Tuple[CommandMetaInterface, ...]:
        return self._subcommands

    def get_parents(self, base_parser: ArgumentParser) -> List[ArgumentParser]:
        return [base_parser]


class RootCommandGroup(CommandGroupBase):
    @property
    def metavar(self) -> str:
        return 'CONTROL'

    @property
    def help(self) -> str:
        return 'Control your LG Smart TV.'

    @property
    def name(self) -> str:
        return 'lgtv-remote'


class ControlCommandBase(CommandBase, ABC):
    def __init__(self, adapter: WebOSClientAdapter, control_type: Type[WebOSControlBase]):
        self.adapter = adapter
        self.control_type = control_type

    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('-n', '--name'),
                'kwargs': {
                    'help': 'The name of an authenticated TV.',
                    'metavar': 'NAME',
                    'dest': 'name'
                }
            },
        )

    def create_control(self, path: str, friendly_name: str) -> WebOSControlBase:
        adapter = self.adapter
        control_type = self.control_type

        return control_type(adapter.create(path, friendly_name))
