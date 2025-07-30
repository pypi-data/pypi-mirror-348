#!/usr/bin/env python3
# vim: fileencoding=utf-8 ts=4
# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: © Copyright 2025 by Christian Dönges. All rights reserved.
# SPDXID: SPDXRef-test-enumaction-py
import argparse
import enum

from pymisclib.enumaction import EnumAction
import pytest


def name_helper(enum_class: enum.Enum,
                argv: list[str|int],
                expected: argparse.Namespace | None):
    """Test EnumAction using the name."""
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument('--name', '-n', type=enum_class,
                        use='name', action=EnumAction)
    if expected is None:
        with pytest.raises(argparse.ArgumentError):
            args = parser.parse_args(argv)
    else:
        args = parser.parse_args(argv)
        assert args == expected


def value_helper(enum_class: enum.Enum,
                argv: list[str|int],
                expected: argparse.Namespace | None):
    """Test EnumAction using the value."""
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument('--value', '-v', type=enum_class,
                        use='value', action=EnumAction)
    if expected is None:
        with pytest.raises(argparse.ArgumentError):
            args = parser.parse_args(argv)
    else:
        args = parser.parse_args(argv)
        assert args == expected


class TestEnum(enum.Enum):
    E1 = 'e1'
    E2 = 'e2'


def test_enumaction_name_enum_ok():
    """Test good cases of using the name of an enum.Enum subclass."""
    name_helper(TestEnum,
                ['--name', 'E1'],
                argparse.Namespace(name=TestEnum.E1))
    name_helper(TestEnum,
                ['-n', 'E2'],
                argparse.Namespace(name=TestEnum.E2))


def test_enumaction_name_enum_err():
    """Test error cases of using the name of an enum.Enum subclass."""
    name_helper(TestEnum, ['--name', 'e1'], None)
    name_helper(TestEnum, ['-n', 'e1'], None)
    name_helper(TestEnum, ['-n', 'does_not_exist'], None)


def test_enumaction_value_enum_ok():
    """Test good cases of using the value of an enum.Enum subclass."""
    value_helper(TestEnum,
                ['--value', 'e1'],
                argparse.Namespace(value=TestEnum.E1))
    value_helper(TestEnum,
                ['-v', 'e2'],
                argparse.Namespace(value=TestEnum.E2))


def test_enumaction_value_enum_err():
    """Test error cases of using the value of an enum.Enum subclass."""
    value_helper(TestEnum, ['--value', 'E1'], None)
    value_helper(TestEnum, ['-v', 'E1'], None)
    value_helper(TestEnum, ['-v', 'does_not_exist'], None)


class TestIntEnum(enum.IntEnum):
    I1 = 1
    I2 = 2


def test_enumaction_name_int_enum_ok():
    """Test good cases of using the name of an enum.IntEnum subclass."""
    name_helper(TestIntEnum,
                ['--name', 'I1'],
                argparse.Namespace(name=TestIntEnum.I1))
    name_helper(TestIntEnum,
                ['-n', 'I2'],
                argparse.Namespace(name=TestIntEnum.I2))


def test_enumaction_name_int_enum_err():
    """Test error cases of using the name of an enum.IntEnum subclass."""
    name_helper(TestEnum, ['--name', 'i1'], None)
    name_helper(TestEnum, ['-n', '1'], None)
    name_helper(TestEnum, ['-n', 'does_not_exist'], None)


def test_enumaction_value_int_enum_err():
    """All cases of using the value of an enum.IntEnum subclass are error cases."""
    value_helper(TestIntEnum, ['--value', '1'], None)
    value_helper(TestIntEnum, ['--value', 'does_not_exist'], None)

    with pytest.raises(TypeError):
        # Python argparse can not handle non-string arguments.
        value_helper(TestIntEnum, ['-v', 1], None)


class TestFlagEnum(enum.Flag):
    F1 = 1
    F2 = 2


def test_enumaction_name_flag_ok():
    """Test good cases of using the name of an enum.IntEnum subclass."""
    name_helper(TestFlagEnum,
                ['--name', 'F1'],
                argparse.Namespace(name=TestFlagEnum.F1))
    name_helper(TestFlagEnum,
                ['-n', 'F2'],
                argparse.Namespace(name=TestFlagEnum.F2))


def test_enumaction_name_flag_err():
    """Test error cases of using the name of an enum.Flag subclass."""
    name_helper(TestEnum, ['--name', 'f1'], None)
    name_helper(TestEnum, ['-n', '1'], None)
    name_helper(TestEnum, ['-n', 'does_not_exist'], None)


def test_enumaction_value_flag_err():
    """All cases of using the value of an enum.FlagEnum subclass are error cases."""
    value_helper(TestIntEnum, ['--value', '1'], None)
    value_helper(TestIntEnum, ['--value', 'does_not_exist'], None)

    with pytest.raises(TypeError):
        # Python argparse can not handle non-string arguments.
        value_helper(TestIntEnum, ['-v', 1], None)


class TestIntFlagEnum(enum.IntFlag):
    IF1 = 1
    IF2 = 2
    IF4 = 4


def test_enumaction_name_int_flag_ok():
    """Test good cases of using the name of an enum.IntFlag subclass."""
    name_helper(TestIntFlagEnum, ['--name', 'IF1'],
                argparse.Namespace(name=TestIntFlagEnum.IF1))
    name_helper(TestIntFlagEnum, ['-n', 'IF2'],
                argparse.Namespace(name=TestIntFlagEnum.IF2))

def test_enumaction_name_int_flag_err():
    """Test error cases of using the name of an enum.IntFlag subclass."""
    name_helper(TestIntEnum, ['--name', '1'], None)
    name_helper(TestIntEnum, ['--name', 'does_not_exist'], None)
    # Multiple flags are not supported.
    name_helper(TestIntFlagEnum, ['-n', 'IF1|IF4'], None)

    with pytest.raises(TypeError):
        # Python argparse can not handle non-string arguments.
        value_helper(TestIntEnum, ['-v', 3], None)
