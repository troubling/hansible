#!/usr/bin/env python
# All this does is look for any device in `/dev/*` that is a symlink and
# creates a map of all the symlinked devices to their actual devices

import json
import os

devmap = {}

for f in os.listdir('/dev'):
    try:
        d = os.readlink('/dev/'+f)
    except:
        continue
    m[f] = d
print(json.dumps(m))
