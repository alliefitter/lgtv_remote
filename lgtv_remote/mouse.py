from argparse import Namespace
from typing import Type, Tuple, Optional

from pywebostv.controls import WebOSControlBase
from pynput.mouse import Controller

from lgtv_remote.agent import MouseAgent, BlockingWindow, KeyboardAgent
from lgtv_remote.command import CommandGroupBase, ControlCommandBase, CommandMetaInterface
from lgtv_remote.factory import WebOSClientFactory


class MouseCommandGroup(CommandGroupBase):
    def __init__(
            self,
            subcommands: Tuple[CommandMetaInterface, ...],
            factory: WebOSClientFactory,
            control_type: Type[WebOSControlBase]
    ):
        super().__init__(subcommands)
        self.factory = factory
        self.control_type = control_type

    @property
    def metavar(self) -> str:
        return 'COMMAND'

    @property
    def help(self) -> str:
        return 'Control the mouse and other buttons of your LG Smart TV.'

    @property
    def name(self) -> str:
        return 'mouse'

    @property
    def subcommands(self) -> Tuple[CommandMetaInterface, ...]:
        buttons = [
            'click',
            'left',
            'right',
            'down',
            'up',
            'home',
            'back',
            'ok',
            'dash',
            'info',
            'one',
            'two',
            'three',
            'four',
            'five',
            'six',
            'seven',
            'eight',
            'nine',
            'zero',
            'asterisk',
            'cc',
            'exit',
            'mute',
            'red',
            'green',
            'blue',
            'volume_up',
            'volume_down',
            'channel_up',
            'channel_down'
        ]
        return self._subcommands + tuple(
            PressButtonCommand(button, self.factory, self.control_type) for button in buttons
        )

    @property
    def usage(self) -> Optional[str]:
        return 'lgtv-remote mouse COMMAND'


class PressButtonCommand(ControlCommandBase):
    def __init__(self, button: str, factory: WebOSClientFactory, control_type: Type[WebOSControlBase]):
        self.button = button
        super().__init__(factory, control_type)

    def execute(self, namespace: Namespace):
        button = self.button
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.connect_input()
        getattr(control, button)(block=True)
        control.disconnect_input()

    @property
    def help(self) -> str:
        return {
            'click': 'Press the button at the center of your remote\'s directional pad.',
            'left': 'Press the left of your remote\'s directional pad.',
            'right': 'Press the right of your remote\'s directional pad.',
            'down': 'Press the down of your remote\'s directional pad.',
            'up': 'Press the up of your remote\'s directional pad.',
            'home': 'Press the home button on your remote.',
            'back': 'Press the back button on your remote.',
            'ok': 'Press the ok on your remote.',
            'dash': 'Press the dash on your remote.',
            'info': 'Press the info on your remote.',
            'one': 'Press the one on your remote.',
            'two': 'Press the two on your remote.',
            'three': 'Press the three on your remote.',
            'four': 'Press the four on your remote.',
            'five': 'Press the five on your remote.',
            'six': 'Press the six on your remote.',
            'seven': 'Press the seven on your remote.',
            'eight': 'Press the eight on your remote.',
            'nine': 'Press the nine on your remote.',
            'zero': 'Press the zero on your remote.',
            'asterisk': 'Press the asterisk on your remote.',
            'cc': 'Press the cc on your remote.',
            'exit': 'Press the exit on your remote.',
            'mute': 'Press the mute on your remote.',
            'red': 'Press the red on your remote.',
            'green': 'Press the green on your remote.',
            'blue': 'Press the blue on your remote.',
            'volume_up': 'Press the volume_up on your remote.',
            'volume_down': 'Press the volume_down on your remote.',
            'channel_up': 'Press the channel_up on your remote.',
            'channel_down': 'Press the channel_down on your remote.'
        }[self.button]

    @property
    def name(self) -> str:
        return self.button


class CaptureMouseCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.connect_input()
        MouseAgent(control, BlockingWindow(Controller())).listen()
        control.disconnect_input()

    @property
    def help(self) -> str:
        return 'Control the mouse on your TV with your computer\'s mouse. Press the mouse\'s right button to exit.'

    @property
    def name(self) -> str:
        return 'capture-mouse'


class CaptureKeyboardCommand(ControlCommandBase):
    def execute(self, namespace: Namespace):
        name = namespace.name
        path = namespace.config_path

        control = self.create_control(path, name)
        control.connect_input()
        KeyboardAgent(control, BlockingWindow(Controller())).listen()
        control.disconnect_input()

    @property
    def help(self) -> str:
        return 'Control your TV\'s keyboard with your computer\'s keyboard. Press the esc button to exit.'

    @property
    def name(self) -> str:
        return 'capture-keyboard'
