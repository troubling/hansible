#!/usr/bin/env python
# Copyright (c) 2018 Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# All this does is look for any device in `/dev/*` that is a symlink and
# creates a map of all the symlinked devices to their actual devices

import json
import os

devmap = {}

for f in os.listdir('/dev'):
    try:
        d = os.readlink('/dev/'+f)
    except Exception:
        devmap[f] = f
        continue
    devmap[f] = d
print(json.dumps(devmap))
