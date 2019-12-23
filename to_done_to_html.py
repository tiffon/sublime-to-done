import sublime, sublime_plugin
import tempfile
import webbrowser
import cgi


class ToDoneToHtmlCommand(sublime_plugin.TextCommand):

    def is_visible(self):
        return "ToDone" in self.view.settings().get ("syntax")

    def run(self, edit):
        selections = self.view.sel()

        texts = []

        for selection in selections:
            if selection.a != selection.b:
                region = self.view.line(sublime.Region(selection.a, selection.b))
                if len(texts) > 0 and (texts[-1][2].b >= region.a):
                    new_region = sublime.Region(texts[-1][2].a, region.b)
                    texts[-1] = [texts[-1][0], self.view.substr(new_region), new_region]
                else:
                    texts.append([self.view.rowcol(region.a)[0] + 1, self.view.substr(region), region])

        text = "\n".join([t[1] for t in texts])

        lines = text.splitlines()

        processed_lines = []

        last_indent = 0
        list_level = 0

        for line in lines:

            if line.strip() == "":
                prefix = "<br>"
                postfix = ""
            elif line.strip().startswith("-") or line.strip().startswith("+"):
                # bulleted
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

            dashes = 0
            if line_nospace.startswith("-5"):
                line_nospace = line_nospace[2:]
                dashes = 5
            elif line_nospace.startswith("-4"):
                line_nospace = line_nospace[2:]
                dashes = 4
            elif line_nospace.startswith("-3"):
                line_nospace = line_nospace[2:]
                dashes = 3
            elif line_nospace.startswith("-2"):
                line_nospace = line_nospace[2:]
                dashes = 2
            elif line_nospace.startswith("-1"):
                line_nospace = line_nospace[2:]
                dashes = 1
            elif line_nospace.startswith("-----"):
                line_nospace = line_nospace[5:]
                dashes = 5
            elif line_nospace.startswith("----"):
                line_nospace = line_nospace[4:]
                dashes = 4
            elif line_nospace.startswith("---"):
                line_nospace = line_nospace[3:]
                dashes = 3
            elif line_nospace.startswith("--"):
                line_nospace = line_nospace[2:]
                dashes = 2
            elif line_nospace.startswith("-"):
                line_nospace = line_nospace[1:]
                dashes = 1

            dash_to_style = {
                0 : "color:blue; font-size: 120%; font-weight: bold;",
                1 : "color:gray;",
                2 : "color:green;",
                3 : "color:purple",
                4 : "color:black; font-size: 100%; font-weight: bold;",
                5 : "color:black; font-size: 110%; font-weight: bold; background-color: #FFFF00"
            }

            prefix = prefix + "<span style=\"%s\">" % dash_to_style[dashes]
            postfix = "</span>" + postfix

            if done:
                prefix = prefix + "<span style=\"color:lightgray;\">"
                postfix = "</span>" + postfix

            if indent > last_indent:
                prefix = "<ul>" + prefix
                list_level = list_level + 1

            if indent < last_indent:
                prefix = "</ul>" + prefix
                list_level = list_level - 1

            processed_lines.append(" " * indent + prefix + cgi.escape(line_nospace) + postfix)
            last_indent = indent

        for l in range(list_level):
            processed_lines.append("</ul>")

        final_text = "\n".join(processed_lines)

        html = "\n".join([
            """
            <html>
            <head>
            <style>
            body {
                font-family:      Helvetica, Arial, FreeSans, san-serif;
                }
            </style>
            </head>
            <body>
            """,
            "<ul>",
            final_text,
            "</ul>",
            "</body>",
            "</html>",
            ])

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        tmp_file.write(bytes(html, 'UTF-8'))
        tmp_file.close()

        webbrowser.open_new_tab(tmp_file.name)


