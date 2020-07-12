from sys import argv

from pywebostv.controls import MediaControl, SystemControl, InputControl

from lgtv_remote.client import Client
from lgtv_remote.command import RootCommandGroup
from lgtv_remote.command_groups.connect import ConnectCommandGroup, AuthenticateCommand, DiscoverCommand, \
    SendCommand
from lgtv_remote.adapter import WebOSClientAdapter
from lgtv_remote.command_groups.media import MediaCommandGroup, VolumeUpCommand, VolumeDownCommand, GetVolumeCommand, SetVolumeCommand, \
    MuteCommand, UnmuteCommand, PlayCommand, PauseCommand, StopCommand, RewindCommand, FastForwardCommand
from lgtv_remote.command_groups.input import InputCommandGroup, CaptureMouseCommand, CaptureKeyboardCommand
from lgtv_remote.settings import Settings
from lgtv_remote.command_groups.system import SystemCommandGroup, NotifyCommand, PowerOnCommand, PowerOffCommand, InfoCommand


def main():
    settings = Settings()
    adapter = WebOSClientAdapter(settings)
    Client(
        RootCommandGroup(
            (
                ConnectCommandGroup(
                    (
                        AuthenticateCommand(
                            adapter
                        ),
                        DiscoverCommand(
                            adapter
                        ),
                        SendCommand(
                            adapter
                        )
                    )
                ),
                MediaCommandGroup(
                    (
                        VolumeUpCommand(
                            adapter,
                            MediaControl
                        ),
                        VolumeDownCommand(
                            adapter,
                            MediaControl
                        ),
                        GetVolumeCommand(
                            adapter,
                            MediaControl
                        ),
                        SetVolumeCommand(
                            adapter,
                            MediaControl
                        ),
                        MuteCommand(
                            adapter,
                            MediaControl
                        ),
                        UnmuteCommand(
                            adapter,
                            MediaControl
                        ),
                        PlayCommand(
                            adapter,
                            MediaControl
                        ),
                        PauseCommand(
                            adapter,
                            MediaControl
                        ),
                        StopCommand(
                            adapter,
                            MediaControl
                        ),
                        RewindCommand(
                            adapter,
                            MediaControl
                        ),
                        FastForwardCommand(
                            adapter,
                            MediaControl
                        )
                    )
                ),
                SystemCommandGroup(
                    (
                        NotifyCommand(
                            adapter,
                            SystemControl
                        ),
                        PowerOnCommand(
                            settings
                        ),
                        PowerOffCommand(
                            adapter,
                            SystemControl
                        ),
                        InfoCommand(
                            adapter,
                            SystemControl
                        )
                    )
                ),
                InputCommandGroup(
                    (
                        CaptureMouseCommand(
                            adapter,
                            InputControl
                        ),
                        CaptureKeyboardCommand(
                            adapter,
                            InputControl
                        )
                    ),
                    adapter,
                    InputControl
                )
            )
        )
    ).run(argv[1:])


if __name__ == '__main__':
    main()
