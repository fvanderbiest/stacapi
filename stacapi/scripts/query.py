#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from ..utils import query

ALLOWED_KEYS = ['lineid', 'stopid', 'direction']

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s lineid=value stopid=value direction=1|2\n'
          '(example: "%s lineid=1606 stopid=2200918 direction=1")' % (cmd, cmd))
    sys.exit(1)


# TODO: options = parse_vars(argv[2:]) with from pyramid.scripts.common import parse_vars ?
def parse(argv):
    a = {}
    for arg in argv[1:]:
        r = arg.split("=")
        if len(r) == 2 and r[0] in ALLOWED_KEYS:
            a[r[0]] = int(r[1])
        else:
            usage(argv)
            break
    return (a['lineid'], a['stopid'], a['direction'])

def main(argv=sys.argv):
    if len(argv) != 4:
        usage(argv)
    
    lineId, stopId, direction = parse(argv)
    
    buses = query(lineId, stopId, direction)
    for nextbus in buses:
        print("Next bus is in {}min{}s, at {}".format(nextbus['min'], nextbus['sec'], nextbus['time']))

    