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


from mkdocs.config import config_options as option
from mkdocs.config.base import Config

from mkdocs_publisher._shared.mkdocs_utils import ConfigChoiceEnum


class SlugModeChoiceEnum(ConfigChoiceEnum):
    TITLE = 0, True, False
    FILENAME = 1, False, False


class _MetaSlugConfig(Config):
    enabled = option.Type(bool, default=True)
    mode = option.Choice(choices=SlugModeChoiceEnum.choices(), default=SlugModeChoiceEnum.default())
    warn_on_missing = option.Type(bool, default=True)
    key_name = option.Type(str, default="slug")


class OverviewChoiceEnum(ConfigChoiceEnum):
    AUTO = 0, True, False
    TRUE = 1, False, True
    FALSE = 2, False, True


class _MetaOverviewConfig(Config):
    default = option.Choice(choices=OverviewChoiceEnum.choices(), default=OverviewChoiceEnum.default())
    enabled = option.Type(bool, default=True)
    key_name = option.Type(str, default="overview")


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


class _MetaPublishConfig(Config):
    dir_default = option.Choice(choices=PublishChoiceEnum.choices(), default=True)
    dir_warn_on_missing = option.Type(bool, default=False)
    file_default = option.Choice(choices=PublishChoiceEnum.choices(), default=False)
    file_warn_on_missing = option.Type(bool, default=True)
    key_name = option.Type(str, default="publish")
    search_in_hidden = option.Type(bool, default=False)
    search_in_draft = option.Type(bool, default=False)


class TitleChoiceEnum(ConfigChoiceEnum):
    META = 0, True, False
    HEAD = 1, False, False
    FILE = 2, False, False


class _MetaTitleConfig(Config):
    key_name = option.Type(str, default="title")
    mode = option.Choice(choices=TitleChoiceEnum.choices(), default=TitleChoiceEnum.default())
    warn_on_missing_header = option.Type(bool, default=True)
    warn_on_missing_meta = option.Type(bool, default=True)


class _MetaRedirectConfig(Config):
    key_name = option.Type(str, default="redirect")


class MetaPluginConfig(Config):
    dir_meta_file = option.Choice(["README.md", "index.md"], default="README.md")

    overview: _MetaOverviewConfig = option.SubConfig(_MetaOverviewConfig)  # type: ignore
    publish: _MetaPublishConfig = option.SubConfig(_MetaPublishConfig)  # type: ignore
    redirect: _MetaRedirectConfig = option.SubConfig(_MetaRedirectConfig)  # type: ignore
    slug: _MetaSlugConfig = option.SubConfig(_MetaSlugConfig)  # type: ignore
    title: _MetaTitleConfig = option.SubConfig(_MetaTitleConfig)  # type: ignore
