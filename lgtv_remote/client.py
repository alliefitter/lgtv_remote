from argparse import ArgumentParser, _SubParsersAction as SubParser
from pathlib import Path
from typing import Tuple, Dict, List

from lgtv_remote.command import CommandGroupInterface, CommandInterface, CommandMetaInterface
from lgtv_remote.exeception import ClientError


class Client:
    options: Tuple[Dict] = (
        {
            'args': ('-c', '--config-path',),
            'kwargs': {
                'dest': 'config_path',
                'help': 'The path to your lgtv-remote configuration file. By default this will be ~/.lgtv.yaml.',
                'metavar': 'CONFIG_PATH',
                'default': Path().home() / '.lgtv.yaml'
            }
        },
    )

    def __init__(self, command_group: CommandGroupInterface):
        self.command_group = command_group
        self.parser: ArgumentParser = ArgumentParser(
            description=command_group.help,
            prog=command_group.name
        )
        self.base_parser = ArgumentParser(add_help=False)

    def run(self, *args):
        try:
            self._run(*args)
        except (KeyboardInterrupt, ClientError) as e:
            if isinstance(e, ClientError):
                print('Error: ', e)
            else:
                print('Exiting...')

    def _run(self, *args):
        self._set_global_options()
        command_group = self.command_group
        subparsers = self.parser.add_subparsers(
            metavar=command_group.metavar,
            help=command_group.help
        )
        self._set_commands(command_group.subcommands, subparsers, command_group.get_parents(self.base_parser))
        namespace = self.parser.parse_args(*args)
        if hasattr(namespace, 'command'):
            command: CommandInterface = namespace.command
            command.execute(namespace)
        elif hasattr(namespace, 'group_help'):
            namespace.group_help()
        else:
            self.parser.print_help()

    def _set_commands(
            self,
            commands: Tuple[CommandMetaInterface],
            subparsers: SubParser,
            parents: List[ArgumentParser]
    ):
        for command in commands:
            command_parser = subparsers.add_parser(
                command.name,
                help=command.help,
                parents=parents if isinstance(command, CommandInterface) else []
            )
            if isinstance(command, CommandInterface):
                self._set_command(command, command_parser)
            elif isinstance(command, CommandGroupInterface):
                command_parser.set_defaults(group_help=command_parser.print_help)
                self._set_command_group(command, command_parser)

    def _set_command(self, command: CommandInterface, command_parser: ArgumentParser):
        for option in command.options:
            command_parser.add_argument(*option.get('args'), **option.get('kwargs'))
        command_parser.set_defaults(
            command=command,
            **command.defaults
        )

    def _set_command_group(
            self,
            command_group: CommandGroupInterface,
            command_parser: ArgumentParser
    ):
        subparsers = command_parser.add_subparsers(
            metavar=command_group.metavar,
            help=command_group.help
        )
        self._set_commands(command_group.subcommands, subparsers, command_group.get_parents(self.base_parser))

    def _set_global_options(self):
        for option in self.options:
            self.base_parser.add_argument(*option.get('args'), **option.get('kwargs'))

