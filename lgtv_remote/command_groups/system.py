from argparse import Namespace
from typing import Tuple, Dict, Optional

from getmac import get_mac_address
from wakeonlan import send_magic_packet

from lgtv_remote.command import ControlCommandBase, CommandGroupBase, CommandBase
from lgtv_remote.settings import SettingsInterface


class SystemCommandGroup(CommandGroupBase):
    @property
    def metavar(self) -> str:
        return 'COMMAND'

    @property
    def help(self) -> str:
        return 'Control the system of your LG Smart TV, such as powering the TV on or off.'

    @property
    def name(self) -> str:
        return 'system'


class NotifyCommand(ControlCommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return super().options + (
            {
                'args': ('message',),
                'kwargs': {
                    'metavar': 'MESSAGE',
                    'help': 'A message to appear in a notification on your TV.'
                }
            },
        )

    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path
        message = namespace.message

        control = self.create_control(path, name)
        control.notify(message, block=True)

    @property
    def help(self) -> str:
        return 'Display a notification on your TV.'

    @property
    def name(self) -> str:
        return 'notify'


class PowerOnCommand(CommandBase):
    def __init__(self, settings: SettingsInterface):
        self.settings = settings

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

    def execute(self, namespace: Namespace):
        settings = self.settings
        name = namespace.name
        path = namespace.config_path

        settings.load(path)
        tv_settings = settings.get(name)

        send_magic_packet(get_mac_address(ip=tv_settings.host))

    @property
    def help(self) -> str:
        return 'Turn on the power of your TV.'

    @property
    def name(self) -> str:
        return 'power-on'


class PowerOffCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.power_off(block=True)

    @property
    def help(self) -> str:
        return 'Turn off the power of your TV.'

    @property
    def name(self) -> str:
        return 'power-off'


class InfoCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        response = control.info(block=True)
        for key, value in response.items():
            print(key, ': ', value)

    @property
    def help(self) -> str:
        return 'Get info about your TV.'

    @property
    def name(self) -> str:
        return 'info'
