from argparse import Namespace
from typing import Tuple, Dict, Optional

from lgtv_remote.command import ControlCommandBase, CommandGroupBase


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

    @property
    def usage(self) -> Optional[str]:
        return 'lgtv-remote system COMMAND'


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


class PowerOnCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.power_on()

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
