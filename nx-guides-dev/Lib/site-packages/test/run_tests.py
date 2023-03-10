import os
import os.path as osp

from pygments import highlight as pygments_highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

from a11y_pygments.utils.utils import find_all_themes


languages = {
    "python": "py",
    "javascript": "js",
    "bash": "bash",
    "html": "html",
    "css": "css",
    "markdown": "md",
    }

themes = find_all_themes()

actdir = osp.dirname(__file__)
outdir = osp.join(actdir, 'results')

if not osp.exists(outdir):
    os.mkdir(outdir)

for language in languages:
    ext = languages[language]
    name = osp.join(actdir, 'scripts', 'test.' + ext)

    with open(name, 'r') as f:
        lines = f.read()

    lexer = get_lexer_by_name(language, stripall=True)

    for theme in themes:
        style = get_style_by_name(theme)
        formatter = HtmlFormatter(style=style, full=True, hl_lines=[2,3,4])
        result = pygments_highlight(lines, lexer, formatter)

        theme_outdir = osp.join(outdir, theme)

        if not osp.exists(theme_outdir):
            os.mkdir(theme_outdir)

        out = osp.join(theme_outdir, ext + '.html')
        with open(out, 'w') as f:
            f.write(result)
