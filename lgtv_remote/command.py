from abc import ABC, abstractmethod
from argparse import Namespace, ArgumentParser
from typing import Optional, Dict, Tuple, List, Type

from pywebostv.controls import WebOSControlBase

from lgtv_remote.factory import WebOSClientFactory


class CommandMetaInterface(ABC):
    @property
    @abstractmethod
    def help(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def usage(self) -> Optional[str]:
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

    @property
    def usage(self) -> Optional[str]:
        return None


class CommandGroupBase(CommandGroupInterface, ABC):
    def __init__(self, subcommands: Tuple[CommandMetaInterface, ...]):
        self._subcommands = subcommands

    @property
    def subcommands(self) -> Tuple[CommandMetaInterface, ...]:
        return self._subcommands

    @property
    def usage(self) -> Optional[str]:
        return None

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

    @property
    def usage(self) -> Optional[str]:
        return 'lgtv-remote CONTROL ...'


class ControlCommandBase(CommandBase, ABC):
    def __init__(self, factory: WebOSClientFactory, control_type: Type[WebOSControlBase]):
        self.factory = factory
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
        factory = self.factory
        control_type = self.control_type

        return control_type(factory.create(path, friendly_name))


class AuthenticateCommand(CommandBase):
    def __init__(self, factory: WebOSClientFactory):
        self.factory = factory

    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('name',),
                'kwargs': {
                    'help': 'A name of the TV with which you are attempting to authenticate, such as "living_room" or '
                            '"bedroom".',
                    'metavar': 'NAME'
                }
            },
            {
                'args': ('ip_address',),
                'kwargs': {
                    'help': 'The IP address of the TV with which you are attempting to authenticate.',
                    'metavar': 'IP_ADDRESS'
                }
            }
        )

    def execute(self, namespace: Namespace):
        factory = self.factory
        name = namespace.name
        ip_address = namespace.ip_address
        path = namespace.config_path

        factory.authenticate(name, ip_address, path)

    @property
    def help(self) -> str:
        return 'Authenticate with an LG smart TV.'

    @property
    def name(self) -> str:
        return 'authenticate'


class DiscoverCommand(CommandBase):
    def __init__(self, factory: WebOSClientFactory):
        self.factory = factory

    @property
    def options(self) -> Tuple[Dict, ...]:
        return tuple()

    def execute(self, namespace: Namespace):
        factory = self.factory

        factory.discover()

    @property
    def help(self) -> str:
        return 'Discover LG smart TVs connected to your network.'

    @property
    def name(self) -> str:
        return 'discover'


