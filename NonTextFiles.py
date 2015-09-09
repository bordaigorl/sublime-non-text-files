import sublime
import sublime_plugin
import subprocess
import os
from fnmatch import fnmatch


def open_file(filepath):
    if sublime.platform() == "osx":
        subprocess.call(('open', filepath))
    elif sublime.platform() == "windows":
        os.startfile(filepath)
    elif sublime.platform() == "linux":
        subprocess.call(('xdg-open', filepath))


class OpenExternallyCommand(sublime_plugin.WindowCommand):

    def run(self, path=None, then_close=False):
        view = self.window.active_view()
        path = path or view.file_name()
        if path:
            open_file(path)
            if then_close:
                if hasattr(view, "close"):
                    view.close()
                else:
                    self.window.run_command("close")
        else:
            view.set_status("NTFiles", "Cannot open file with external application")
            sublime.set_timeout(lambda: view.erase_status("NTFiles"), 10000)

    def is_enabled(self):
        if self.window.active_view():
            return self.window.active_view().file_name() is not None
        else:
            return False


class OpenFileExternally(sublime_plugin.EventListener):

    def on_load(self, view):
        path = view.file_name()
        if not path:
            return
        for gpat in view.settings().get("open_externally_patterns", []):
            if fnmatch(path, gpat):
                open_file(path)


class PreventBinPreview(sublime_plugin.EventListener):
    last_path = None

    def on_load(self, view):
        win = view.window() or sublime.active_window()
        if win and view.settings().get("prevent_bin_preview", True):
            path = view.file_name()
            if path and self.last_path != path:
                for gpat in view.settings().get("binary_file_patterns", []):
                    if fnmatch(path, gpat):
                        if hasattr(view, "close"):
                            view.close()
                        else:
                            sublime.set_timeout(lambda: win.run_command("close"), 0)
            self.last_path = path
