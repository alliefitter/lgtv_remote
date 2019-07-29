from sys import argv

from pywebostv.controls import MediaControl, SystemControl, InputControl

from lgtv_remote.client import Client
from lgtv_remote.command import RootCommandGroup, AuthenticateCommand, DiscoverCommand
from lgtv_remote.factory import WebOSClientFactory
from lgtv_remote.media import MediaCommandGroup, VolumeUpCommand, VolumeDownCommand, GetVolumeCommand, SetVolumeCommand, \
    MuteCommand, UnmuteCommand, PlayCommand, PauseCommand, StopCommand, RewindCommand, FastForwardCommand
from lgtv_remote.mouse import MouseCommandGroup, CaptureMouseCommand, CaptureKeyboardCommand
from lgtv_remote.settings import Settings
from lgtv_remote.system import SystemCommandGroup, NotifyCommand, PowerOnCommand, PowerOffCommand, InfoCommand


def main():
    factory = WebOSClientFactory(Settings())
    Client(
        RootCommandGroup(
            (
                AuthenticateCommand(
                    factory
                ),
                DiscoverCommand(
                    factory
                ),
                MediaCommandGroup(
                    (
                        VolumeUpCommand(
                            factory,
                            MediaControl
                        ),
                        VolumeDownCommand(
                            factory,
                            MediaControl
                        ),
                        GetVolumeCommand(
                            factory,
                            MediaControl
                        ),
                        SetVolumeCommand(
                            factory,
                            MediaControl
                        ),
                        MuteCommand(
                            factory,
                            MediaControl
                        ),
                        UnmuteCommand(
                            factory,
                            MediaControl
                        ),
                        PlayCommand(
                            factory,
                            MediaControl
                        ),
                        PauseCommand(
                            factory,
                            MediaControl
                        ),
                        StopCommand(
                            factory,
                            MediaControl
                        ),
                        RewindCommand(
                            factory,
                            MediaControl
                        ),
                        FastForwardCommand(
                            factory,
                            MediaControl
                        )
                    )
                ),
                SystemCommandGroup(
                    (
                        NotifyCommand(
                            factory,
                            SystemControl
                        ),
                        PowerOnCommand(
                            factory,
                            SystemControl
                        ),
                        PowerOffCommand(
                            factory,
                            SystemControl
                        ),
                        InfoCommand(
                            factory,
                            SystemControl
                        )
                    )
                ),
                MouseCommandGroup(
                    (
                        CaptureMouseCommand(
                            factory,
                            InputControl
                        ),
                        CaptureKeyboardCommand(
                            factory,
                            InputControl
                        )
                    ),
                    factory,
                    InputControl
                )
            )
        )
    ).run(argv[1:])


if __name__ == '__main__':
    main()
