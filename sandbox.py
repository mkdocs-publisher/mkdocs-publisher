import re

ANCHOR_RE_PART = r"((#(?P<anchor>([^|\][()'\"]+)))?)"
EXTRA_RE_PART = r"( *({(?P<extra>[\w+=. ]+)})?)"
IMAGE_RE_PART = r"((\|(?P<image>([0-9x]+)))?)"
LINK_RE_PART = r"(?P<link>(?!(https?|ftp)://)[^|#()\s]+)"
URL_RE_PART = r"(?P<link>((https?|ftp)://)?[\w\-]{2,}\.[\w\-]{2,}(\.[\w\-]{2,})?([^\s\][)(]*))"
TEXT_RE_PART = r"(?P<text>[^\][)(|]+)"
LINK_TITLE_RE_PART = r"( \"(?P<title>[ \S]+)\")?"

HTTP_LINK_RE = re.compile(rf"\[{TEXT_RE_PART}]\({URL_RE_PART}\)")
WIKI_LINK_RE = re.compile(rf"(?<!!)\[\[{LINK_RE_PART}{ANCHOR_RE_PART}(\|{TEXT_RE_PART})?]]")
WIKI_EMBED_LINK_RE = re.compile(
    rf"!\[\[{LINK_RE_PART}{ANCHOR_RE_PART}{IMAGE_RE_PART}]]{EXTRA_RE_PART}"
)
MD_LINK_RE = re.compile(
    rf"(?<!!)\[{TEXT_RE_PART}]\({LINK_RE_PART}{ANCHOR_RE_PART}{LINK_TITLE_RE_PART}\)"
)
MD_EMBED_LINK_RE = re.compile(
    rf"!\[{TEXT_RE_PART}]\({LINK_RE_PART}{LINK_TITLE_RE_PART}\){EXTRA_RE_PART}"
)
RELATIVE_LINK_RE = re.compile(
    rf"\[{TEXT_RE_PART}]\({LINK_RE_PART}{ANCHOR_RE_PART}{LINK_TITLE_RE_PART}\)"
)

MARKDOWN_LINK_RE = re.compile(r"\[([^][\r\n]+)]\(((?!https?://)[^][)(\s]+.md)(#[\w\S]+)?\)")
HTTP_LINK_RE_B = re.compile(r"\[([^][\r\n]+)]\((https?://[^][)(\s]+)(#[\w\-.]+)?\)")

print(MD_LINK_RE)
print(MARKDOWN_LINK_RE)
print("")
print(HTTP_LINK_RE)
print(HTTP_LINK_RE_B)
