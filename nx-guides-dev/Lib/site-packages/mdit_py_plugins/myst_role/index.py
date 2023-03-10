import re

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.rules_inline import StateInline

VALID_NAME_PATTERN = re.compile(r"^\{([a-zA-Z0-9\_\-\+\:]+)\}")


def myst_role_plugin(md: MarkdownIt):
    """Parse ``{role-name}`content```"""
    md.inline.ruler.before("backticks", "myst_role", myst_role)
    md.add_render_rule("myst_role", render_myst_role)


def myst_role(state: StateInline, silent: bool):
    # check name
    match = VALID_NAME_PATTERN.match(state.src[state.pos :])
    if not match:
        return False
    name = match.group(1)

    # check for starting backslash escape
    try:
        if state.srcCharCode[state.pos - 1] == 0x5C:  # /* \ */
            # escaped (this could be improved in the case of edge case '\\{')
            return False
    except IndexError:
        pass

    # scan opening tick length
    start = pos = state.pos + match.end()
    try:
        while state.src[pos] == "`":
            pos += 1
    except IndexError:
        return False

    tick_length = pos - start
    if not tick_length:
        return False

    # search for closing ticks
    match = re.search("`" * tick_length, state.src[pos + 1 :])
    if not match:
        return False
    content = state.src[pos : pos + match.start() + 1].replace("\n", " ")

    if not silent:
        token = state.push("myst_role", "", 0)
        token.meta = {"name": name}
        token.content = content

    state.pos = pos + match.end() + 1

    return True


def render_myst_role(self, tokens, idx, options, env):
    token = tokens[idx]
    name = token.meta.get("name", "unknown")
    return f'<code class="myst role">{{{name}}}[{escapeHtml(token.content)}]</code>'
