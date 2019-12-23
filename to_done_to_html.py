"""
Simple update to the ToDone plugin to export ToDos to HTML. This is useful if you want to share
your TODOs via email.

This script by Anjul Patney (Original plugin here: https://github.com/tiffon/sublime-to-done)
"""
import html
import tempfile
import webbrowser
import sublime
import sublime_plugin

class ToDoneToHtmlCommand(sublime_plugin.TextCommand):
    """ToDone to HTML Class"""

    def __init__(self, view):
        super().__init__(view)
        self.indent_level_map = {0 : 0}

    def is_visible(self):
        """Return true if syntax is ToDone"""
        return "ToDone" in self.view.settings().get("syntax")

    def run(self, edit):
        """Main plugin code. Collect the current selection(s) and export to HTML"""

        del edit

        lines = self.get_selected_text().splitlines()

        processed_lines = []

        last_list_level = 0
        list_level = 0

        self.parse_indents(lines)

        for line in lines:
            if line.strip() == "":
                prefix = "<br>"
                postfix = ""
            elif line.strip().startswith("-") or line.strip().startswith("+"):
                prefix = "<li>"
                postfix = "</li>"
            else:
                prefix = ""
                postfix = ""

            line_nospace = line.lstrip()

            indent = len(line) - len(line_nospace)

            done = False
            if line_nospace.startswith("+"):
                done = True
                line_nospace = line_nospace[1:]
                # prefix = prefix + "[DONE]"

            dashes, line_nospace = get_todo_level(line_nospace)

            prefix = prefix + "<span style=\"%s\">" % dash_to_style(dashes)
            postfix = "</span>" + postfix

            if done:
                prefix = prefix + "<span style=\"color:lightgray;\">"
                postfix = "</span>" + postfix

            list_level = self.indent_level_map[indent]

            if list_level > last_list_level:
                prefix = "<ul>" * (list_level - last_list_level) + "\n" + prefix

            if list_level < last_list_level:
                prefix = "</ul>" * (last_list_level - list_level) + "\n" + prefix

            processed_lines.append(" " * indent + prefix + html.escape(line_nospace) + postfix)
            last_list_level = list_level

        for _ in range(list_level):
            processed_lines.append("</ul>")

        final_text = "<ul>\n" + "\n".join(processed_lines) + "</ul>"

        show_in_browser(final_text)

    def parse_indents(self, lines):
        """Parse how indentations should correspond to HTML list levels"""
        indent_levels = [0]
        for line in lines:
            spaces = len(line) - len(line.lstrip())
            if spaces not in indent_levels:
                indent_levels.append(spaces)

        level = 0
        print(self.indent_level_map)
        for spaces in sorted(indent_levels):
            self.indent_level_map[spaces] = level
            level = level + 1

    def get_selected_text(self):
        """returns the current selection as one string"""
        selections = self.view.sel()

        texts = []

        # The below snippet taken from
        # https://github.com/grubernaut/sublimetext-print-to-html
        for selection in selections:
            if selection.a != selection.b:
                region = self.view.line(sublime.Region(selection.a, selection.b))
                if len(texts) > 0 and (texts[-1][2].b >= region.a):
                    new_region = sublime.Region(texts[-1][2].a, region.b)
                    texts[-1] = [texts[-1][0], self.view.substr(new_region), new_region]
                else:
                    texts.append(
                        [self.view.rowcol(region.a)[0] + 1, self.view.substr(region), region])

        return "\n".join([t[1] for t in texts])

def get_todo_level(line):
    """Convert line prefix to TODO level"""
    line_nospace = line.lstrip()
    retval = None
    if line_nospace.startswith("-5"):
        retval = 5, line_nospace[2:]
    elif line_nospace.startswith("-4"):
        retval = 4, line_nospace[2:]
    elif line_nospace.startswith("-3"):
        retval = 3, line_nospace[2:]
    elif line_nospace.startswith("-2"):
        retval = 2, line_nospace[2:]
    elif line_nospace.startswith("-1"):
        retval = 1, line_nospace[2:]
    elif line_nospace.startswith("-----"):
        retval = 5, line_nospace[5:]
    elif line_nospace.startswith("----"):
        retval = 4, line_nospace[4:]
    elif line_nospace.startswith("---"):
        retval = 3, line_nospace[3:]
    elif line_nospace.startswith("--"):
        retval = 2, line_nospace[2:]
    elif line_nospace.startswith("-"):
        retval = 1, line_nospace[1:]
    else:
        retval = 0, line_nospace

    return retval

def dash_to_style(dash_count):
    """Convert TODO level to a CSS style statement"""
    style_dict = {
        0 : "color:blue; font-size: 120%; font-weight: bold;",
        1 : "color:gray;",
        2 : "color:green;",
        3 : "color:purple",
        4 : "color:black; font-size: 100%; font-weight: bold;",
        5 : "color:black; font-size: 110%; font-weight: bold; background-color: #FFFF00"
    }

    return style_dict[dash_count]

def show_in_browser(body_html):
    """Write HTML to a temp file, then show in browser"""

    full_html = "\n".join([
        """
        <html>
        <head>
        <style>
        body { font-family: Helvetica, Arial, FreeSans, san-serif; }
        </style>
        </head>
        <body>
        """,
        body_html,
        """
        </body>
        </html>
        """
        ])

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    tmp_file.write(bytes(full_html, 'UTF-8'))
    tmp_file.close()

    webbrowser.open_new_tab(tmp_file.name)
