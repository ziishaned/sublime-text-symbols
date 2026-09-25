import sublime

from . import aliases
from . import icons
from . import themes

from .overlay import with_ignored_overlay
from .utils.decorators import debounce
from .utils.logging import log
from .utils.path import PACKAGE_NAME, OVERLAY_ROOT

PACKAGE_SETTINGS = "A File Icon.sublime-settings"
USER_SETTINGS = "Preferences.sublime-settings"

_cached_packages = []
_cached_settings = {}
_uuid = "9ebcce78-4cac-4089-8bd7-d551c634b052"


def add_listener():
    log("Initializing settings")
    path = "Packages/{0}/{1}".format(PACKAGE_NAME, PACKAGE_SETTINGS)
    package_settings = sublime.load_settings(PACKAGE_SETTINGS)
    for key in sublime.decode_value(sublime.load_resource(path)).keys():
        if key not in ("dev_mode", "dev_trace"):
            _cached_settings[key] = package_settings.get(key)

    user_settings = sublime.load_settings(USER_SETTINGS)
    _cached_packages = user_settings.get("ignored_packages")

    icons.init()
    themes.patch(_cached_settings)
    aliases.check(_cached_settings["aliases"])

    package_settings.add_on_change(_uuid, _on_change_package)
    user_settings.add_on_change(_uuid, _on_change_user)


def clear_listener():
    sublime.load_settings(PACKAGE_SETTINGS).clear_on_change(_uuid)
    sublime.load_settings(USER_SETTINGS).clear_on_change(_uuid)


@debounce(100)
def _on_change_package():
    is_aliases_changed = False
    is_icons_changed = False
    is_force_mode_changed = False

    settings = sublime.load_settings(PACKAGE_SETTINGS)

    for key, value in _cached_settings.items():
        new_value = settings.get(key)
        if value != new_value:
            _cached_settings[key] = new_value
            if key == "aliases":
                is_aliases_changed = True
            elif key == "force_mode":
                is_force_mode_changed = True
            else:
                is_icons_changed = True

    if is_aliases_changed:
        log("Aliases settings changed")
        aliases.check(_cached_settings["aliases"])
    if is_icons_changed:
        log("Icons settings changed")
        themes.patch(_cached_settings, overwrite=True)
    elif is_force_mode_changed:
        log("Force mode settings changed")
        themes.patch(_cached_settings)


def _on_change_user():
    global _cached_packages
    settings = sublime.load_settings(USER_SETTINGS)
    packages = settings.get("ignored_packages", [])
    if OVERLAY_ROOT in packages:
        packages.remove(OVERLAY_ROOT)
    if packages != _cached_packages:
        _cached_packages = packages

        @debounce(2000)
        def update_overlay():
            themes.patch(_cached_settings, on_demand=True)
            aliases.check(_cached_settings["aliases"], on_demand=True)

        update_overlay()
