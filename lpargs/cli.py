from __future__ import absolute_import

import argparse
from argparse import Namespace
import sys
from collections import deque

from lpargs.parser import LArgsParser
from shlex import quote


def parse_args():
    raw_args = deque(sys.argv)
    args = Namespace(brackets='{}', delimiter=',', template=[])
    raw_args.popleft()
    while raw_args:
        arg = raw_args.popleft()
        if arg in {'-d', '--delimiter'}:
            args.delimiter = raw_args.popleft()
        elif arg in {'-b', '--brackets'}:
            args.brackets = raw_args.popleft()
        else:
            args.template = [arg] + list(raw_args)
            break
    return args


def main():
    args = parse_args()

    template = ' '.join(
        quote(arg).replace('\-', '-')
        for arg in args.template
    )

    begin_bracket, end_bracket = args.brackets

    parser = LArgsParser(
        template=template,
        delimiter=args.delimiter,
        begin_bracket=begin_bracket,
        end_bracket=end_bracket,
    )

    for line in sys.stdin:
        line = line.strip()
        res = parser.sub(line)
        print(res)

if __name__ == '__main__':
    main()
