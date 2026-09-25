import json
import os
import shutil

import sublime

from itertools import chain

from .utils import path
from .utils.colors import convert_color_value
from .utils.logging import log, dump

from . import icons


def patch(settings, overwrite=False, on_demand=False):
    theme_packages = _installed_themes()
    themes = set((theme for theme in chain(*theme_packages.values())))
    try:
        if on_demand and patch.themes == themes:
            return
    except Exception:
        pass
    patch.themes = themes

    supported = [] if settings.get("force_mode") else _customizable_themes()

    general_patch = _create_general_patch(settings)
    specific_patch = _create_specific_patch(settings)

    general = path.overlay_patches_general_path()
    specific = path.overlay_patches_specific_path()

    color = "single" if settings.get("color") else "multi"
    general_dest = os.path.join(general, color)

    patched = set()

    if theme_packages:
        log("Patching themes")
        for package, themes in theme_packages.items():
            if package in supported:
                icons.copy_missing(general, specific, package)
                patched.update(
                    _patch_themes(
                        themes,
                        os.path.join(specific, package, color),
                        specific_patch,
                        overwrite,
                    )
                )
            else:
                patched.update(
                    _patch_themes(themes, general_dest, general_patch, overwrite)
                )
    else:
        log("No themes to patch!")

    log("Removing obsolete theme patches")
    for dirpath, dirnames, filenames in os.walk(path.overlay_patches_path()):
        if dirpath == specific:
            for filepath in set(dirnames) - set(supported):
                filepath = os.path.join(dirpath, filepath)
                shutil.rmtree(filepath, ignore_errors=True)
                dump(filepath)

        for filename in filenames:
            if filename.endswith(".sublime-theme"):
                filepath = os.path.join(dirpath, filename)
                if filepath not in patched:
                    try:
                        os.remove(filepath)
                        dump(filepath)
                    except OSError:
                        pass


def _customizable_themes():
    log("Getting the list of theme packages with customization support")

    customizable = set()
    for res in sublime.find_resources(".supports-a-file-icon-customization"):
        if not res.startswith("Packages/"):
            continue

        _, package, _ = res.split("/")
        customizable.add(package)

    dump(customizable)
    return customizable


def _installed_themes():
    log("Getting installed themes")

    found_themes = set()
    theme_packages = {}

    for res in sublime.find_resources("*.sublime-theme"):
        if not res.startswith("Packages/"):
            continue

        _, package, *_, theme = res.split("/")
        if package != path.OVERLAY_ROOT:
            if theme not in found_themes:
                found_themes.add(theme)
                theme_packages.setdefault(package, []).append(theme)

    dump(theme_packages)
    return theme_packages


def _patch_themes(themes, dest, text, overwrite):
    patched = set()
    mode = "w" if overwrite else "x"
    for theme in themes:
        try:
            filename = os.path.join(dest, theme)
            patched.add(filename)
            with open(filename, mode) as t:
                t.write(text)
        except FileExistsError:
            log("Ignored `{}`".format(theme))
        except Exception as error:
            log("Error patching `{}`".format(theme))
            dump(error)
        else:
            log("Patched `{}`".format(theme))
    return patched


def _create_general_patch(settings):
    log("Preparing general patch")
    theme_content = []

    row_padding = settings.get("row_padding")
    if row_padding:
        theme_content.append({"class": "sidebar_tree", "row_padding": row_padding})

    color = convert_color_value(settings.get("color"))
    opacity = settings.get("opacity")
    icon = _patch_icon(None, color, opacity)

    size = settings.get("size")
    if size:
        icon["content_margin"] = [size, size]

    theme_content.append(icon)

    color = convert_color_value(settings.get("color_on_hover"))
    opacity = settings.get("opacity_on_hover")
    if color or opacity:
        theme_content.append(_patch_icon("hover", color, opacity))

    color = convert_color_value(settings.get("color_on_select"))
    opacity = settings.get("opacity_on_select")
    if color or opacity:
        theme_content.append(_patch_icon("selected", color, opacity))

    theme_content.extend(_create_folder_patch(settings))

    dump(theme_content)
    return json.dumps(theme_content)


def _create_specific_patch(settings):
    log("Preparing specific patch")
    theme_content = []

    row_padding = settings.get("row_padding")
    if row_padding:
        theme_content.append({"class": "sidebar_tree", "row_padding": row_padding})

    color = convert_color_value(settings.get("color"))
    icon = _patch_icon(None, color)

    size = settings.get("size")
    if size:
        icon["content_margin"] = [size, size]

    theme_content.append(icon)

    if color:
        color_on_hover = convert_color_value(settings.get("color_on_hover"))
        if color_on_hover:
            theme_content.append(_patch_icon("hover", color_on_hover))

        color_on_select = convert_color_value(settings.get("color_on_select"))
        if color_on_select:
            theme_content.append(_patch_icon("selected", color_on_select))

    dump(theme_content)
    return json.dumps(theme_content)


def _patch_icon(attrib, color=None, opacity=None):
    """Built an icon theme rule

    :attrib:
        The tree row's state attribute the returned rule applies to.
    :color:
        The color to tint the icon with.
        It is always required to override any theme settings. The default value of
        `none` removes any tinting specified by a theme to display colored icons.
    :opacity:
        If specified overwrites theme's opacity setting.
    """
    icon = {"class": "icon_file_type", "layer0.tint": color}
    if attrib:
        icon["parents"] = [{"class": "tree_row", "attributes": [attrib]}]
    if opacity is not None:
        icon["layer0.opacity"] = opacity
    return icon


def _create_folder_patch(settings):
    """Build the theme rules, which replace the folder icons.

    The folder icons don't support per state tints as most themes tint them
    differently for light and dark windows. Therefore the light window rule
    of colored folder icons is neutralized, too.
    """
    variant = "single" if settings.get("color") else "multi"
    opacity = settings.get("opacity")
    color = convert_color_value(settings.get("color"))
    size = settings.get("size") or 8

    def folder_icon(texture, attrib=None):
        icon = {
            "class": "icon_folder",
            "layer0.texture": texture,
            "layer0.tint": color,
        }
        if attrib:
            icon["parents"] = [{"class": "tree_row", "attributes": [attrib]}]
        else:
            # square margin to preserve the icon's aspect ratio
            icon["content_margin"] = [size, size]
        if opacity is not None:
            icon["layer0.opacity"] = opacity
        return icon

    icons_path = "{}/icons/folders/{}".format(path.PACKAGE_NAME, variant)
    theme_content = [
        folder_icon(icons_path + "/folder.png"),
        folder_icon(icons_path + "/folder_open.png", attrib="expanded"),
    ]

    # Neutralize light theme tints to preserve the colored folder icons.
    if variant == "multi":
        icon = folder_icon(icons_path + "/folder.png")
        icon["parents"] = [{"class": "window", "attributes": ["file_light"]}]
        theme_content.insert(1, icon)

    return theme_content
