#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2024 zhaosonggo@gmail.com, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

from plugin_cli.plugin.plugin import Plugin


class PluginManager:
    def __init__(self):
        self.plugins = {}

    def register_plugin(self, plugin: Plugin):
        self.plugins[plugin.name] = plugin

    def dispatch_args(self, args):
        plugin = self.plugins[args.plugin]
        return plugin.accept(args)
