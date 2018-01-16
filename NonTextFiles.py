import sublime
import sublime_plugin
import subprocess
import os
from fnmatch import fnmatch


def open_file(filepath):
    if sublime.platform() == "osx":
        subprocess.Popen(('open', filepath))
    elif sublime.platform() == "windows":
        os.startfile(filepath)
    elif sublime.platform() == "linux":
        subprocess.Popen(('xdg-open', filepath))


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

class NonTextFilesRightClickCommand(sublime_plugin.WindowCommand):

    def run(self, **kw):
        pass

    def is_visible(self, **kw):
        OpenFileExternally.bypass = True
        return False


def enableOpenFileExternally():
    OpenFileExternally.bypass = False


class OpenFileExternally(sublime_plugin.EventListener):

    bypass = False

    def on_load(self, view):
        # I reset the bypass flag with a timeout to fail gracefully
        # if ST calls the `is_visible` method after the `on_load` event.
        sublime.set_timeout(enableOpenFileExternally, 500)
        if OpenFileExternally.bypass:
            return
        path = view.file_name()
        if not path:
            return
        for gpat in view.settings().get("open_externally_patterns", []):
            if fnmatch(path, gpat):
                open_file(path)
                break


class PreventBinPreview(sublime_plugin.EventListener):
    last_path = None

    def reset_path(self):
        self.last_path = None

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
                        break
            self.last_path = path
        sublime.set_timeout(lambda: self.reset_path(), 500)
