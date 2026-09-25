import sys
import sublime
import sublime_plugin

if int(sublime.version()) >= 3114:
    __all__ = ["AfiRevertCommand", "plugin_loaded", "plugin_unloaded"]

    # Clear module cache to force reloading all modules of this package.
    prefix = __package__ + "."  # don't clear the base package
    for module_name in [
        module_name
        for module_name in sys.modules
        if module_name.startswith(prefix) and module_name != __name__
    ]:
        del sys.modules[module_name]
    del prefix

    from .core import aliases
    from .core import overlay
    from .core import settings

    class AfiRevertCommand(sublime_plugin.ApplicationCommand):
        def run(self):
            def remove_aliases():
                try:
                    aliases.disable()
                finally:
                    overlay.disable_overlay()
                    sublime.set_timeout_async(remove_overlay, overlay.IGNORE_DELAY)

            def remove_overlay():
                try:
                    overlay.clear_overlay()
                finally:
                    settings.add_listener()
                    overlay.enable_overlay()

            settings.clear_listener()
            sublime.set_timeout_async(remove_aliases)

    def plugin_loaded():
        def setup_overlay():
            settings.add_listener()
            overlay.enable_overlay()

        # run delayed to prevent race condition with previous plugin_unloaded
        sublime.set_timeout_async(setup_overlay, 1000)

    def plugin_unloaded():
        settings.clear_listener()
        aliases.disable()
        overlay.safe_clear_overlay()

else:
    raise ImportWarning("Doesn't support Sublime Text versions prior to 3114")
