import sublime
import sublime_plugin
from os.path import basename

# Attempt to load urllib.request/error and fallback to urllib2 (Python 2/3 compat)
try:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.parse import urlencode
    from urllib.error import URLError
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request, URLError


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
            ScalariverFormat(view, edit).format(sel)


class ScalariverFile(sublime_plugin.TextCommand):

    def run(self, edit):
        sel = sublime.Region(0, self.view.size())
        ScalariverFormat(self.view, edit).format(sel)


class ScalariverFormat:

    def __init__(self, view, edit):
        self.view = view
        self.edit = edit

    def get_config(self, original):
        settings = self.view.settings()
        url = settings.get("scalariver_url") or "http://river.scalex.org"
        config = settings.get("scalariver_options") or {}
        config.update({"source": original})
        return (url, config)

    def format(self, region):
        original = self.view.substr(region)
        formated = self.call_scalariver(original)
        self.view.replace(self.edit, region, formated)

    def call_scalariver(self, original):
        try:
            (url, data) = self.get_config(original)
            params = urlencode(data).encode('utf-8')
            request = Request(url, params, headers={"User-Agent": "Sublime Scalariver"})
            http_file = urlopen(request, timeout=5)
            return http_file.read().decode('utf-8')
        except URLError as err:
            # Otherwise, if there was a connection error, let it be known
            sublime.status_message('Error connecting to "%s"' % url)
            return original


class ScalariverListener(sublime_plugin.EventListener):
    '''This listener allow to format on save
    '''

    def __init__(self):
        super(ScalariverListener, self).__init__()

    def on_post_save(self, view):
        if view.settings().get("scalariver_formatonsave"):
            view.window().run_command('scalariver_file')
