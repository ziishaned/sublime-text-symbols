import os
import sublime

PACKAGE_NAME, *_ = __package__.split(".", 1)
OVERLAY_ROOT = "{0} {1}".format("zzz", PACKAGE_NAME)


def makedirs(*args):
    absolute_path = os.path.join(*args)
    os.makedirs(absolute_path, exist_ok=True)
    return absolute_path


def installed_package_path():
    return os.path.join(
        sublime.installed_packages_path(), PACKAGE_NAME + ".sublime-package"
    )


def package_icons_path():
    return os.path.join(sublime.packages_path(), PACKAGE_NAME, "icons")


def overlay_path():
    return os.path.join(sublime.packages_path(), OVERLAY_ROOT)


def overlay_cache_path():
    return os.path.join(sublime.cache_path(), OVERLAY_ROOT)


def overlay_aliases_path(file_name=""):
    return os.path.join(sublime.packages_path(), OVERLAY_ROOT, "aliases", file_name)


def overlay_patches_path():
    return os.path.join(sublime.packages_path(), OVERLAY_ROOT, "patches")


def overlay_patches_general_path():
    return os.path.join(sublime.packages_path(), OVERLAY_ROOT, "patches", "general")


def overlay_patches_specific_path():
    return os.path.join(sublime.packages_path(), OVERLAY_ROOT, "patches", "specific")


def overlay_aliases_resource_path(file_name=""):
    return "Packages/{}/aliases/{}".format(OVERLAY_ROOT, file_name)
