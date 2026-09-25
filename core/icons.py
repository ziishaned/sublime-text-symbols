import json
import os
import shutil
import zipfile

import sublime

from .utils import path
from .utils.logging import log, dump


def init():
    log("Initializing icons")

    try:
        # create hidden overlay package
        overlay_path = path.overlay_path()
        os.makedirs(overlay_path, exist_ok=True)
        open(os.path.join(overlay_path, ".hidden-sublime-package"), "a").close()

        general_path = path.overlay_patches_general_path()
        if os.path.isdir(general_path):
            dump("All the necessary icons are provided")
        else:
            _init_overlay(general_path)
    except Exception as error:
        log("Error during copy")
        dump(error)


def copy_missing(source, overlay, package):
    log("Checking icons for {}...".format(package))

    try:
        missing_icons = _get_missing(package)
        if missing_icons:
            _copy_missing(source, overlay, package, "multi", missing_icons)
            _copy_missing(source, overlay, package, "single", missing_icons)
        return bool(missing_icons)
    except OSError as error:
        log("Error during copy")
        dump(error)
    return False


def _init_overlay(dest):
    """Create the icon overlay package.

    In order to make sure to override existing icons provided by the themes
    icons need to be copied to a package, which is loaded as late as possible.

    This function therefore creates a package named `zzz A File Icon zzz` and
    copies all icons over there.
    """
    # copy icons from the loosen package folder
    src = path.package_icons_path()
    _copy_general(src, dest, "multi")
    _copy_general(src, dest, "single")

    # extract remaining icons from the package archive
    package = path.installed_package_path()
    try:
        source_paths = ("icons/multi/", "icons/single/")

        with zipfile.ZipFile(package) as z:
            for m in z.namelist():
                if not any(m.startswith(p) for p in source_paths):
                    continue

                _, name = m.split("/", 1)
                if not name.endswith(".png"):
                    continue

                try:
                    with open(os.path.join(dest, name), "xb") as f:
                        f.write(z.read(m))
                except FileExistsError:
                    pass
                except FileNotFoundError as error:
                    dump(error)

        dump("Icons extracted from ", package)
    except FileNotFoundError:
        dump("No icons found in ", package)


def _copy_general(source, overlay, color):
    src = os.path.join(source, color)
    dest = os.path.join(overlay, color)
    try:
        shutil.copytree(src, dest)
        dump("Icons copied from ", src)
    except FileNotFoundError:
        dump("No icons found in ", src)
        os.makedirs(dest, exist_ok=True)
    except OSError as error:
        log("Error during copy")
        dump(error)


def _copy_missing(source, overlay, package, color, icons):
    src = os.path.join(source, color)
    dest = path.makedirs(overlay, package, color)
    suffixes = (".png", "@2x.png", "@3x.png")
    for icon in icons:
        for suffix in suffixes:
            _copy(src, dest, icon + suffix)


def _copy(src, dest, icon):
    try:
        with open(os.path.join(dest, icon), "xb") as df:
            with open(os.path.join(src, icon), "rb") as sf:
                df.write(sf.read())
    except FileExistsError:
        pass


def _get_missing(package):
    package_icons = icons_json_content()
    theme_icons_path = _icons_path(package)
    if not theme_icons_path:
        return package_icons

    theme_icons = {
        os.path.basename(os.path.splitext(i)[0])
        for i in sublime.find_resources("*.png")
        if i.startswith(theme_icons_path)
    }

    return [icon for icon in package_icons if icon not in theme_icons]


def _icons_path(package):
    package_path = "Packages/" + package
    for res in sublime.find_resources("file_type_default.png"):
        if res.startswith(package_path):
            return os.path.dirname(res)
    return False


def icons_json_content():
    try:
        # Cache content to keep it available as we need it
        # to clear aliases, if package is unloaded.
        return icons_json_content.cache
    except AttributeError:
        try:
            icons_json = json.loads(
                sublime.load_resource(
                    "Packages/" + path.PACKAGE_NAME + "/icons/icons.json"
                )
            )
            icons_json_content.cache = icons_json
            return icons_json
        except FileNotFoundError as e:
            log(e)
            return {}
