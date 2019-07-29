from argparse import Namespace
from typing import Tuple, Dict, Optional

from lgtv_remote.command import CommandGroupBase, ControlCommandBase


class MediaCommandGroup(CommandGroupBase):
    @property
    def metavar(self) -> str:
        return 'COMMAND'

    @property
    def help(self) -> str:
        return 'Control media on your LG Smart TV, such as changing volume or pausing video.'

    @property
    def name(self) -> str:
        return 'media'

    @property
    def usage(self) -> Optional[str]:
        return 'lgtv-remote media COMMAND'


class VolumeUpCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.volume_up(block=True)

    @property
    def help(self) -> str:
        return 'Increase your TV\'s volume by one.'

    @property
    def name(self) -> str:
        return 'volume-up'


class VolumeDownCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.volume_down(block=True)

    @property
    def help(self) -> str:
        return 'Decrease your TV\'s volume by one.'

    @property
    def name(self) -> str:
        return 'volume-down'


class GetVolumeCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        response = control.get_volume(block=True)
        for key, value in response.items():
            print(key, ': ', value)

    @property
    def help(self) -> str:
        return 'Get the current volume level of your TV.'

    @property
    def name(self) -> str:
        return 'get-volume'


class SetVolumeCommand(ControlCommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return super().options + (
            {
                'args': ('level',),
                'kwargs': {
                    'metavar': 'LEVEL',
                    'type': int
                }
            },
        )

    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path
        level = namespace.level

        control = self.create_control(path, name)
        control.set_volume(level, block=True)

    @property
    def help(self) -> str:
        return 'Set the volume of your TV.'

    @property
    def name(self) -> str:
        return 'set-volume'


class MuteCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.mute(True, block=True)

    @property
    def help(self) -> str:
        return 'Mute the volume on your TV.'

    @property
    def name(self) -> str:
        return 'mute'


class UnmuteCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.mute(False, block=True)

    @property
    def help(self) -> str:
        return 'Unmute the volume on your TV.'

    @property
    def name(self) -> str:
        return 'unmute'


class PlayCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.play(block=True)

    @property
    def help(self) -> str:
        return 'Play current video displayed on your TV.'

    @property
    def name(self) -> str:
        return 'play'


class PauseCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.pause(block=True)

    @property
    def help(self) -> str:
        return 'Pause the current video displayed on your TV.'

    @property
    def name(self) -> str:
        return 'pause'


class StopCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.stop(block=True)

    @property
    def help(self) -> str:
        return 'Stop the current video displayed on your TV.'

    @property
    def name(self) -> str:
        return 'stop'


class RewindCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.rewind(block=True)

    @property
    def help(self) -> str:
        return 'Rewind the current video displayed on your TV.'

    @property
    def name(self) -> str:
        return 'rewind'


class FastForwardCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.fast_forward(block=True)

    @property
    def help(self) -> str:
        return 'Fast forward the current video displayed on your TV.'

    @property
    def name(self) -> str:
        return 'fast-forward'
