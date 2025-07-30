# Copyright 2024 zhaosonggo@gmail.com, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

from typing import Callable


class CLIDescription:
    def __init__(self, name, description, version_callback: Callable[[], str]):
        self.name = name
        self.description = description
        self.version = version_callback
