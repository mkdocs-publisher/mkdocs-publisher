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

from mkdocs.config import config_options as option
from mkdocs.config.base import Config

from mkdocs_publisher._shared.mkdocs_utils import ConfigChoiceEnum


class _SocialOpenGraphConfig(Config):
    enabled = option.Type(bool, default=True)
    locale = option.Type(str, default="en_US")


class _SocialTwitterConfig(Config):
    enabled = option.Type(bool, default=True)
    website = option.Type(str, default="")
    author = option.Type(str, default="")


class _SocialMetaKeysConfig(Config):
    title_key = option.Type(str, default="title")
    description_key = option.Type(str, default="description")
    image_key = option.Type(str, default="image")


class TitleLocationChoiceEnum(ConfigChoiceEnum):
    NONE = 0, False, False
    BEFORE = 1, False, False
    AFTER = 2, True, False


class _SocialSiteNameInTitleConfig(Config):
    location = option.Choice(choices=TitleLocationChoiceEnum.choices(), default=TitleLocationChoiceEnum.default())
    delimiter = option.Type(str, default=" - ")


class SocialConfig(Config):
    meta_keys: _SocialMetaKeysConfig = option.SubConfig(_SocialMetaKeysConfig)  # type: ignore
    og: _SocialOpenGraphConfig = option.SubConfig(_SocialOpenGraphConfig)  # type: ignore
    twitter: _SocialTwitterConfig = option.SubConfig(_SocialTwitterConfig)  # type: ignore
    site_name_in_title: _SocialSiteNameInTitleConfig = option.SubConfig(_SocialSiteNameInTitleConfig)  # type: ignore
