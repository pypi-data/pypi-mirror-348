#!/usr/bin/env python3
# vim: fileencoding=utf-8 ts=4
# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: © Copyright 2025 by Christian Dönges. All rights reserved.
# SPDXID: SPDXRef-time-t-py
"""Timestamp conversion tool."""

import argparse
import enum
import sys

from pymisclib.enumaction import EnumAction
from pymisclib.utilities import convert_timestamp_to_datetime, dir_path, initialize_console, iso8601_str, \
    logging_initialize


class TimestampFormat(enum.Enum):
    """Format of a timestamp."""
    Seconds = 's'
    Milliseconds = 'ms'
    Microseconds = 'µs'
    DotNet = '.net'


def parse_command_line_arguments(argv: list):
    """Parses the command line arguments specified in the argv array and
        returns an object containing all recognized options.

        Unrecognized options will be reported as an error.

        :param list argv: the command-line arguments as supplied by sys.argv[1:].
    """
    parser = argparse.ArgumentParser(description='Timestamp conversion tool.')
    parser.add_argument('timestamps', metavar='TIMESTAMPS',
                        type=str, nargs='+',
                        help='Timestamps to convert. Can be decimal (1, 3.4), or hexadecimal (0x345).')
    parser.add_argument('--format', '-f', action=EnumAction,
                        type=TimestampFormat, use='value',
                        help='Format of the timestamps.')
    args = parser.parse_args(argv)

    return args


def main(argv: list) -> int:
    """Do something useful."""
    # Initialize (Windows) console to use UTF-8.
    initialize_console()

    # Handle command line arguments.
    args = parse_command_line_arguments(argv[1:])

    # Do something useful here.
    if args.format == TimestampFormat.Seconds:
        seconds_digits = 0
    elif args.format == TimestampFormat.Milliseconds:
        seconds_digits = 3
    elif args.format == TimestampFormat.Microseconds:
        seconds_digits = 6
    elif args.format == TimestampFormat.DotNet:
        seconds_digits = 7
    else:
        raise ValueError(f'Timestamp format {args.format.name} is not supported.')

    nr_errors = 0
    timestamps = args.timestamps
    in_values = []
    max_len = 0
    for timestamp in timestamps:
        sd = seconds_digits
        try:
            if '.' in timestamp:
                ts = float(timestamp)
                sd = len(timestamp.split('.')[1])
            else:
                try:
                    ts = int(timestamp)
                except ValueError:
                    prefix = timestamp[:2].lower()
                    bases = {
                        '0b': 2,
                        '0o': 8,
                        '0x': 16
                    }
                    base = bases.get(prefix, 0)
                    if base < 2:
                        raise ValueError(f'unable to convert {timestamp} to a number')
                    ts = int(timestamp, base)
            in_values.append((ts, sd))
            max_len = max(max_len, len(str(ts)))
        except ValueError as e:
            print(f'ERROR: {timestamp} is not a number: {e}', file=sys.stderr)
            nr_errors += 1
            continue

    for ts, sd in in_values:
        try:
            dt = convert_timestamp_to_datetime(ts, args.format.value)
            print(f'{str(ts):{max_len}s} → {iso8601_str(dt, sd)}')
        except ValueError as e:
            nr_errors += 1
            print(f'ERROR: {ts} is not a valid timestamp: {e}', file=sys.stderr)

    return nr_errors


if __name__ == '__main__':
    sys.exit(main(sys.argv))
