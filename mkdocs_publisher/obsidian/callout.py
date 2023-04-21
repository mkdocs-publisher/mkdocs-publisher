import logging
import re

from mkdocs_publisher.obsidian.config import _ObsidianCalloutsConfig

log = logging.getLogger("mkdocs.plugins.publisher.obsidian.callout")

CALLOUT_BLOCK = re.compile(r"^ *(( ?>)+) *\[!([^]]*)]([\-+]?) *(.*)?")
CALLOUT_BLOCK_FOLLOW = re.compile(r"^ *(( ?>)+) *(.*)?")

CALLOUT_MAPPING = {
    "abstract": ["abstract", "summary", "tldr"],
    "bug": ["bug"],
    "example": ["example"],
    "danger": ["danger", "error"],
    "failure": ["fail", "failure", "missing"],
    "info": ["info"],
    "question": ["faq", "help", "question"],
    "quote": ["cite", "quote"],
    "tip": ["hint", "important", "tip"],
    "todo": ["todo"],
    "success": ["check", "done", "success"],
    "warning": ["attention", "caution", "warning"],
}
ADMONITION_MAPPING = {
    callout: admonition for admonition, callouts in CALLOUT_MAPPING.items() for callout in callouts
}
INDENTATION_MAPPING = {
    "tabs": "\t",
    "spaces": "    ",
}
FOLDABILITY_MAPPING = {
    "": "!!!",
    "-": "???",
    "+": "???+",
}
ALIGN_MAPPING = {"left": " inline", "right": " inline end"}


def _callout_indentation(
    match: re.Match, match_group: int, text_indentation: str = "spaces"
) -> str:
    initial_indentation = "".join(" " for _ in range(match.start(match_group)))
    indentation = "".join(
        INDENTATION_MAPPING.get(text_indentation, "spaces")
        for _ in range(match.group(match_group).count(">") - 1)
    )
    return f"{initial_indentation}{indentation}"


def _callout_block(match: re.Match, text_indentation: str = "spaces") -> str:
    # TODO: add possibility to inject customized callout/admonition from CSS/config

    indentation = _callout_indentation(
        match=match, match_group=1, text_indentation=text_indentation
    )

    callout_type = match.group(3).lower()
    if "|" in callout_type:
        callout_type, align = callout_type.split("|")
        align = ALIGN_MAPPING.get(align)
        if align is None:
            log.warning(
                f"Wrong alignment type '{align}'"
                f"(fallback to no alignment, possible values {ALIGN_MAPPING.keys()})"
            )
            align = ""
    else:
        align = ""

    admonition_type = ADMONITION_MAPPING.get(callout_type)
    if admonition_type is None:
        log.warning(f"There is no callout mapping for '{match.group(3)}' (fallback to 'note')")
        admonition_type = "note"

    foldable = FOLDABILITY_MAPPING.get(match.group(4))
    if foldable is None:
        log.warning(f"Wrong definition of foldable '{match.group(4)}' (fallback to non foldable")
        foldable = "!!!"

    title = match.group(5)
    if title and title not in ['""', "''"]:
        title = f'"{title}"'

    return f"{indentation}{foldable} {admonition_type}{align} {title}\n"


def _callout_block_follow(match: re.Match, text_indentation: str = "spaces") -> str:
    indentation = _callout_indentation(
        match=match, match_group=1, text_indentation=text_indentation
    )
    return f"    {indentation} {match.group(3)}"


class CalloutToAdmonition:
    def __init__(self, callouts_config: _ObsidianCalloutsConfig):
        self._callouts_config: _ObsidianCalloutsConfig = callouts_config

    def convert_callouts(self, markdown: str) -> str:
        in_callout_block: bool = False
        markdown_lines = []
        for line in markdown.split("\n"):
            callout_match = re.match(CALLOUT_BLOCK, line)
            callout_follow_match = re.match(CALLOUT_BLOCK_FOLLOW, line)
            if callout_match:
                in_callout_block = True
                markdown_lines.append(
                    _callout_block(
                        match=callout_match, text_indentation=self._callouts_config.indentation
                    )
                )
            elif in_callout_block and callout_follow_match:
                markdown_lines.append(
                    _callout_block_follow(
                        match=callout_follow_match,
                        text_indentation=self._callouts_config.indentation,
                    )
                )
            else:
                in_callout_block = False
                markdown_lines.append(line)

        return "\n".join(line for line in markdown_lines)
