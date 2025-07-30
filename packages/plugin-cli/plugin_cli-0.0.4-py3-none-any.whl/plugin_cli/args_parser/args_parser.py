# Copyright 2024 zhaosonggo@gmail.com, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

import argparse

from plugin_cli.args_parser.cli_description import CLIDescription
from plugin_cli.plugin.plugin import Plugin


class ArgsParser:
    def __init__(self, description: CLIDescription):
        self.parser = argparse.ArgumentParser(description=description.description)
        self.subparsers = self.parser.add_subparsers(
            dest="plugin", help="Available plugins"
        )
        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"{description.name} version {description.version()}",
            help=f"print the {description.name} version number and exit (also --version)",
        )

    def init_subparsers(self, plugins: dict[str, Plugin]):
        for name in plugins:
            subparser = self.subparsers.add_parser(name, help=plugins[name].help())
            plugins[name].build_command_args(subparser)

    def parse_args(self):
        return self.parser.parse_args()

    def print_help(self):
        self.parser.print_help()
