# MIT License
#
# Copyright (c) 2023-2024 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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

from enum import Enum
from typing import cast


class ConfigChoiceEnum(Enum):
    def __eq__(self, other) -> bool:
        if isinstance(other, bool) and self.is_bool:
            return self._str_to_bool(self.name) is other
        return self.name.lower() == str(other).lower()

    def __hash__(self):
        return super().__hash__()

    @staticmethod
    def _str_to_bool(text) -> bool:
        if text.lower() == "true":
            return True
        if text.lower() == "false":
            return False
        raise ValueError(f"'{text}' cannot be converted into bool value")

    @classmethod
    def _get_enums(cls, enums: list) -> list:
        enums_list = []
        for enum in enums:
            if enum.is_bool:
                enums_list.extend([enum.name, cls._str_to_bool(enum.name)])
            else:
                enums_list.append(enum.name)
        return enums_list

    @property
    def name(self) -> str:
        return ".".join(str(self).split(".")[1:]).lower()

    @property
    def is_bool(self) -> bool:
        return self.value[2]

    @classmethod
    def default(cls) -> str | None:
        defaults = [f.name for f in cls if f.value[1]]
        if len(defaults) == 0:
            return None
        if len(defaults) > 1:
            raise ValueError(f"Multiple defaults specified: {defaults}")
        return defaults[0]

    @classmethod
    def choices(cls) -> list:
        return cls._get_enums(enums=cast(list, cls))


class OverviewChoiceEnum(ConfigChoiceEnum):
    AUTO = 0, True, False
    TRUE = 1, False, True
    FALSE = 2, False, True


class PublishChoiceEnum(ConfigChoiceEnum):
    DRAFT = 0, False, False
    HIDDEN = 1, False, False
    PUBLISHED = 2, False, False
    TRUE = 3, False, True
    FALSE = 4, False, True

    @classmethod
    def drafts(cls) -> list:
        return cls._get_enums([cls.DRAFT, cls.FALSE])  # pragma: no cover

    @classmethod
    def published(cls) -> list:
        return cls._get_enums([cls.PUBLISHED, cls.TRUE])  # pragma: no cover


class SlugModeChoiceEnum(ConfigChoiceEnum):
    TITLE = 0, True, False
    FILENAME = 1, False, False


class SocialTitleLocationChoiceEnum(ConfigChoiceEnum):
    NONE = 0, False, False
    BEFORE = 1, False, False
    AFTER = 2, True, False


class TitleChoiceEnum(ConfigChoiceEnum):
    META = 0, True, False
    HEAD = 1, False, False
    FILE = 2, False, False
