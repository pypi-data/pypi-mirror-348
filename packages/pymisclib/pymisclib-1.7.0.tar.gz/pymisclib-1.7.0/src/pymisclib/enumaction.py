#!/usr/bin/env python3
# vim: fileencoding=utf-8 ts=4
# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: © Copyright 2025 by Christian Dönges. All rights reserved.
# SPDXID: SPDXRef-enumaction-py
"""Argparse action for using enum as a choice.

Why would you want to do this if there is already the `choice`

Using it is a simple process.

1. To use it, define an enum subclass with your choices.

.. code-block:: python
    class FooEnum(enum.Enum):
        Foo = 'foo'
        Bar = 'bar'

2. Add an argument to the parser and specify a kwarg `type` with the enum
subclass as value and `action` with value `EnumAction`. Optionally, add a
kwarg `use` with value `name` [default] or `value` to use the enum name or
value, respectively, to match the argument to an enum member.

.. code-block:: python

    parser = argparse.ArgumentParser()
    parser.add_argument('--foo', '-f', type=FooEnum, action=EnumAction)
    parser.add_argument('--bar', '-b', type=FooEnum, use='value', action=EnumAction)

3. Finally, call the :py:func`parse_args()` function of the parser.

Inspired by https://stackoverflow.com/a/60750535.

.. versionadded:: 1.7.0
"""

import argparse
import enum
from pprint import pformat


class EnumAction(argparse.Action):
    """Argparse action for handling Enums"""

    def __init__(self, **kwargs):
        """Initialize the instance.

            Keyword arguments:
                - *type* Specify an :py:type:`enum.Enum` subclass. [required]
                - *use* Either "name" or "value". [optional]
        """
        # Get and check the required 'type' argument.
        enum_type = kwargs.pop('type', None)
        if enum_type is None:
            raise ValueError(f'kwarg "type" missing in {self.__class.__name__}')
        if not issubclass(enum_type, enum.Enum):
            raise TypeError(f'kwarg "type" must specify an enum.Enum subclass in {self.__class.__name__}')
        self._enum_type = enum_type

        # Get and check the optional 'use' argument.
        enum_use = kwargs.pop('use', 'name').lower()
        if enum_use not in ('name', 'value'):
            raise ValueError(f'kwarg "use" must be "name" or "value" in {self.__class.__name__}')
        self._use_name = (enum_use == 'name')

        # Generate choices from the given enum.
        if self._use_name:
            kwargs.setdefault('choices', tuple(e.name for e in enum_type))
        else:
            kwargs.setdefault('choices', tuple(e.value for e in enum_type))

        # Perform the rest of the instance initialization.
        super(EnumAction, self).__init__(**kwargs)

    def __call__(self, parser: argparse.ArgumentParser,
                 namespace: argparse.Namespace,
                 values,
                 option_string:str=None):
        """Perform the action.

        :param argparse.ArgumentParser parser: The parser object containing
             this action.
        :param argparse.Namespace namespace: The namespace object returned by
             :py:func:`parse_args()`.
        :param values: The associated command-line arguments, with any
            type conversions applied. Type conversions are specified with the
            `type` keyword argument to :py:func:`add_argument()`.
        :param str option_string: The option string that was used to invoke
            this action. The option_string argument is optional, and will be
            absent if the action is associated with a positional argument.
        """
        if self._use_name:
            value = self._enum_type[values]
        else:
            value = self._enum_type(values)
        setattr(namespace, self.dest, value)


def example():
    """Example usage."""
    class FooEnum(enum.Enum):
        Foo = 'foo'
        Bar = 'bar'

    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument('--name', '-n', type=FooEnum, action=EnumAction)
    parser.add_argument('--value', '-v', type=FooEnum, use='value', action=EnumAction)

    # Good case.
    argv = ['--name=Foo', '-v', 'bar']
    print(f'Argv  : {pformat(argv)}')
    args = parser.parse_args(argv)
    print(f'Result: {pformat(args)}')

    # Use value instead of name.
    argv = ['-n', 'foo']
    print(f'Argv  : {pformat(argv)}')
    try:
        parser.parse_args(argv)
    except argparse.ArgumentError as e:
        print(e)

    # Use name instead of value
    argv = ['--value', 'Foo']
    print(f'Argv  : {pformat(argv)}')
    try:
        parser.parse_args(argv)
    except argparse.ArgumentError as e:
        print(e)

    argv = ['-n', 'blat']
    print(f'Argv  : {pformat(argv)}')
    try:
        parser.parse_args(argv)
    except argparse.ArgumentError as e:
        print(e)


if __name__ == '__main__':
    example()
