# Copyright 2024 zhaosonggo@gmail.com, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree
from plugin_cli.args_parser.args_parser import ArgsParser
from plugin_cli.args_parser.args_parser import CLIDescription
from plugin_cli.plugin.plugin import Plugin
from plugin_cli.plugin.plugin_manager import PluginManager


class CustomPlugin(Plugin):
    def __init__(self):
        super().__init__("Custom-Plugin")

    def accept(self, args):
        print(args)

    def help(self):
        return "This is a demo plugin."

    def build_command_args(self, subparser):
        subparser.add_argument("subparser", type=str, help="This is a subparser")


def version_callback():
    return "0.0.1"


def main():
    plugin_manager = PluginManager()
    plugin_manager.register_plugin(CustomPlugin())
    description = CLIDescription("demo-cli", "This is a demo cli!", version_callback)
    args_parser = ArgsParser(description)
    args_parser.init_subparsers(plugin_manager.plugins)
    args = args_parser.parse_args()

    if args.plugin is not None:
        plugin_manager.dispatch_args(args)
    else:
        args_parser.print_help()


if __name__ == "__main__":
    main()
