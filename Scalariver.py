import sublime
import sublime_plugin
from os.path import basename


class Scalariver(sublime_plugin.TextCommand):

    def __init__(self, view):
        self.view = view
        self.language = self.get_language()

    def get_language(self):
        syntax = self.view.settings().get('syntax')
        if syntax is None:
            language = "plain text"
        else:
            language = basename(syntax).replace('.tmLanguage', '').lower()
        return language

    def check_enabled(self, lang):
        return lang == "scala"

    def is_enabled(self):
        """
        Enables or disables the 'format' command.
        Command will be disabled if current file is not 'scala'.
        This helps clarify to the user about when the command can be executed,
        especially useful for UI controls.
        """
        return self.check_enabled(self.get_language())

    def run(self, edit):
        """
        Main plugin logic for the 'format' command.
        """
        view = self.view
        regions = view.sel()
        sels = []
        # if there are more than 1 region or region one and it's not empty
        if len(regions) > 1 or not regions[0].empty():
            for region in view.sel():
                if not region.empty():
                    sels.append(region)
        else:  # format all text
            sels.append(sublime.Region(0, view.size()))

        # We start one thread per selection so we don't lock up the interface
        # while waiting for the response from the API
        for sel in sels:
            original = view.substr(sel)
            formated = self.format(original)
            view.replace(edit, sel, formated)

    def format(self, string):
        return string

