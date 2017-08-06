# -*- coding:utf-8 -*-

import sys
import json


with open(sys.argv[1]) as fp:
    infos = list()
    tmp = {}
    for idx, line in enumerate(fp):
        if (idx + 1) % 11 == 0:
            infos.append(tmp)
            tmp = {}
        else:
            key, value = line.strip().split(':', 1)
            tmp[key] = value

print(json.dumps(infos, indent=2))
