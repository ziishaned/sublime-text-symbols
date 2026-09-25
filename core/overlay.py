import shutil
import sublime

from .utils import path
from .utils.logging import log, dump

IGNORE_DELAY = 100


def with_ignored_overlay(fun):
    def decorator(*args, **kwargs):
        def delayed():
            try:
                fun(*args, **kwargs)
            finally:
                enable_overlay()

        disable_overlay()
        sublime.set_timeout_async(delayed, IGNORE_DELAY)

    return decorator


@with_ignored_overlay
def safe_clear_overlay():
    clear_overlay()


def clear_overlay():
    log("Cleaning overlay")

    def handler(function, path, excinfo):
        if handler.success:
            handler.success = False
            log("Error during cleaning")
        dump(path)

    handler.success = True

    shutil.rmtree(path.overlay_path(), onerror=handler)

    if handler.success:
        log("Cleaned overlay successfully")

    return handler.success


def disable_overlay():
    prefs = sublime.load_settings("Preferences.sublime-settings")
    ignored = prefs.get("ignored_packages", [])
    if path.OVERLAY_ROOT not in ignored:
        prefs.set("ignored_packages", ignored + [path.OVERLAY_ROOT])
        sublime.save_settings("Preferences.sublime-settings")


def enable_overlay():
    prefs = sublime.load_settings("Preferences.sublime-settings")
    ignored = prefs.get("ignored_packages", [])
    if path.OVERLAY_ROOT in ignored:
        ignored.remove(path.OVERLAY_ROOT)
        prefs.set("ignored_packages", ignored)
        sublime.save_settings("Preferences.sublime-settings")
