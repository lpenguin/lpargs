from __future__ import absolute_import

import argparse
import sys
from lpargs.parser import LArgsParser
from shlex import quote


def main():
    p = argparse.ArgumentParser(description="Possible operators:\n"
                                            "* {index}: take row with index = {index}\n"
                                            "* e: strip extension\n"
                                            "* E: take extension\n"
                                            "* b: basename\n"
                                            "* d: dirname")
    p.add_argument('--delimiter', '-d', default='\t')
    p.add_argument('--brackets', '-b', default='{}')
    p.add_argument('template', nargs="+",
                   )
    args = p.parse_args()

    template = ' '.join(
        quote(arg)
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
