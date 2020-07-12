import json
from argparse import Namespace
from typing import Tuple, Dict

from lgtv_remote.action import JsonInputAction
from lgtv_remote.command import CommandGroupBase, CommandBase
from lgtv_remote.adapter import WebOSClientAdapter


class ConnectCommandGroup(CommandGroupBase):
    @property
    def metavar(self) -> str:
        return 'COMMAND'

    @property
    def help(self) -> str:
        return 'Discover, connect, and authenticate with your TV.'

    @property
    def name(self) -> str:
        return 'connect'


class AuthenticateCommand(CommandBase):
    def __init__(self, adapter: WebOSClientAdapter):
        self.adapter = adapter

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
        adapter = self.adapter
        name = namespace.name
        ip_address = namespace.ip_address
        path = namespace.config_path

        adapter.authenticate(name, ip_address, path)

    @property
    def help(self) -> str:
        return 'Authenticate with an LG smart TV.'

    @property
    def name(self) -> str:
        return 'authenticate'


class DiscoverCommand(CommandBase):
    def __init__(self, adapter: WebOSClientAdapter):
        self.adapter = adapter

    @property
    def options(self) -> Tuple[Dict, ...]:
        return tuple()

    def execute(self, namespace: Namespace):
        adapter = self.adapter

        adapter.discover()

    @property
    def help(self) -> str:
        return 'Discover LG smart TVs connected to your network.'

    @property
    def name(self) -> str:
        return 'discover'


class SendCommand(CommandBase):
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
            {
                'args': ('uri',),
                'kwargs': {
                    'help': 'The URI of a command, such as "ssap://media.controls/play".',
                    'metavar': 'URI'
                }
            },
            {
                'args': ('params',),
                'kwargs': {
                    'help': 'The URI of a command, such as "ssap://media.controls/play".',
                    'metavar': 'params',
                    'default': None,
                    'action': JsonInputAction,
                    'nargs': '?'
                }
            }
        )

    def __init__(self, adapter: WebOSClientAdapter):
        self.adapter = adapter

    def execute(self, namespace: Namespace):
        adapter = self.adapter
        name = namespace.name
        path = namespace.config_path
        uri = namespace.uri

        client = adapter.create(path, name)
        queue = client.send_message('request', uri, {}, get_queue=True)
        response = queue.get(timeout=60, block=True)
        if response:
            try:
                print(json.dumps(response))
            except ValueError:
                print(response)

    @property
    def help(self) -> str:
        return 'Send a command'

    @property
    def name(self) -> str:
        return 'send'
