# MIT License
#
# Copyright (c) 2023-2025 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Union

import pytest

from mkdocs_publisher._shared.mkdocs_utils import ConfigChoiceEnum


class ConfigChoiceEnumTest(ConfigChoiceEnum):
    DEFAULT = 0, True, False
    FIRST = 1, False, False
    SECOND = 2, False, False
    TRUE = 3, False, True
    FALSE = 4, False, True

    @classmethod
    def bools(cls) -> list:
        return cls._get_enums([cls.TRUE, cls.FALSE])

    @classmethod
    def texts(cls) -> list:
        return cls._get_enums([cls.FIRST, cls.SECOND])


def test_config_choices():
    assert ConfigChoiceEnumTest.choices() == [
        "default",
        "first",
        "second",
        "true",
        True,
        "false",
        False,
    ]


def test_get_bool_enums():
    assert ConfigChoiceEnumTest.bools() == ["true", True, "false", False]


def test_get_text_enums():
    assert ConfigChoiceEnumTest.texts() == ["first", "second"]


def test_get_default():
    assert ConfigChoiceEnumTest.default() == "default"


@pytest.mark.parametrize(
    "enum,expected",
    {
        (ConfigChoiceEnumTest.TRUE, True),
        (ConfigChoiceEnumTest.TRUE, "true"),
        (ConfigChoiceEnumTest.FALSE, False),
        (ConfigChoiceEnumTest.FALSE, "false"),
        (ConfigChoiceEnumTest.FIRST, "first"),
        (ConfigChoiceEnumTest.FIRST, "First"),
        (ConfigChoiceEnumTest.FIRST, "FIRST"),
        (ConfigChoiceEnumTest.FIRST, ConfigChoiceEnumTest.FIRST),
    },
)
def test_eg(enum: ConfigChoiceEnumTest, expected: Union[str, bool]):
    assert enum == expected


def test_no_defaults():
    class NoDefaultChoicesEnum(ConfigChoiceEnum):
        NO_DEFAULT = 0, False, False

    assert NoDefaultChoicesEnum.default() is None


def test_multiple_defaults():
    class MultipleDefaultChoicesEnum(ConfigChoiceEnum):
        FIRST_DEFAULT = 0, True, False
        SECOND_DEFAULT = 1, True, False

    with pytest.raises(ValueError):
        MultipleDefaultChoicesEnum.default()


def test_non_bool_as_bool():
    class NoneBoolChoicesEnum(ConfigChoiceEnum):
        NON_BOOL = 0, False, True

    with pytest.raises(ValueError):
        NoneBoolChoicesEnum.NON_BOOL.choices()
