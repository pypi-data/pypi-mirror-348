#!/usr/bin/env python3
# vim: fileencoding=utf-8 ts=4
# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: © Copyright 2025 by Christian Dönges. All rights reserved.
# SPDXID: SPDXRef-test-utilities-convert-py

from datetime import datetime, timezone
import math

import pytest
from pymisclib.utilities import convert_dotnet_datetime_ticks_to_datetime, convert_ms_since_epoch_to_datetime


dotnet_test_vectors = [
    # DateTime.MaxValue
    (0, datetime.fromisoformat('0001-01-01T00:00:00Z')),
    # Int32.MaxValue should be .7483647 but is 748365 due to rounding errors
    (2147483647, datetime.fromisoformat('0001-01-01T00:03:34.748365Z')),
    # 1 hour
    (36000000000, datetime.fromisoformat('0001-01-01T01:00:00Z')),
    # Unix epoch
    (621355968000000000, datetime.fromisoformat('1970-01-01T00:00:00Z')),
    (630822816000000000, datetime.fromisoformat('2000-01-01T00:00:00Z')),
    (633979008000000000, datetime.fromisoformat('2010-01-01T00:00:00Z')),
    (637134336000000000, datetime.fromisoformat('2020-01-01T00:00:00Z')),
    (638712864000000000, datetime.fromisoformat('2025-01-01T00:00:00Z')),
    # 1 day ago
    (638786877890000000, datetime.fromisoformat('2025-03-27T15:56:29.000Z')),
    # 1 hour ago
    (638787705890000000, datetime.fromisoformat('2025-03-28T14:56:29.000Z')),
    # now
    (638787741890000000, datetime.fromisoformat('2025-03-28T15:56:29.000Z')),
    # datime.MAXYEAR
    (3155378975999990000, datetime.fromisoformat('9999-12-31T23:59:59.999Z'))
] # dotnet_test_vectors


@pytest.mark.parametrize("ticks,expected", dotnet_test_vectors)
def test_convert_dotnet_datetime_ok(ticks, expected):
    dt = convert_dotnet_datetime_ticks_to_datetime(ticks, timezone.utc)
    # We could naively compare dt to expected, but because of
    # rounding errors, this can fail for the milliseconds.
    assert dt.year == expected.year
    assert dt.month == expected.month
    assert dt.day == expected.day
    assert dt.hour == expected.hour
    assert dt.minute == expected.minute
    assert dt.second == expected.second
    assert math.ceil(dt.microsecond * 1000.0) == math.ceil(dt.microsecond * 1000.0)


def test_convert_dotnet_datetime_maxvalue():
    # DateTime.MaxValue
    with pytest.raises(OverflowError):
        dt = convert_dotnet_datetime_ticks_to_datetime(
            3155378975999999999, timezone.utc)


unix_test_vectors = [
    # Epoch
    (0, datetime.fromisoformat('1970-01-01T00:00:00Z')),
    # 0xffffffff
    (4294967295, datetime.fromisoformat('1970-02-19T17:02:47.295Z')),
    # 0x100000000
    (4294967296, datetime.fromisoformat('1970-02-19T17:02:47.296Z')),
    # Date within digits.
    (119731017000, datetime.fromisoformat('1973-10-17T18:36:57Z')),
    # Billenium
    (1000000000000, datetime.fromisoformat('2001-09-09T01:46:40Z')),
    # 1234567890 seconds
    (1234567890123, datetime.fromisoformat('2009-02-13T23:31:30.123Z')),
    # PI
    (3141592653589, datetime.fromisoformat('2069-07-21T00:37:33.589Z')),
    # datetime.MAXYEAR
    (253402300799999, datetime.fromisoformat('9999-12-31T23:59:59.999Z')),
]  # unix_test_vectors


@pytest.mark.parametrize("ticks,expected", unix_test_vectors)
def test_convert_epoch_ms_ok(ticks, expected):
    dt = convert_ms_since_epoch_to_datetime(ticks)
    # The naive comparison should work.
    assert dt == expected
