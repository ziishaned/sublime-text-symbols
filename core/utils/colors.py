import colorsys
import re
import sublime

from ..vendor import webcolors


def convert_color_value(color):
    # ST 3152+ understands css style colors directly
    if int(sublime.version()) >= 3152:
        # convert empty string to None to clear tint
        return color if color else None

    # color: [255, 255, 255]
    try:
        return [int(color[0]), int(color[1]), int(color[2])]
    except:
        # color: hsl(360, 100%, 100%)
        try:
            return _parse_hsl_color(color)
        except:
            # color: "white" or "#fff"
            try:
                return webcolors.html5_parse_legacy_color(color)
            except:
                return None


def _parse_hsl_color(color):
    h, s, l = re.match(r"hsl\(\s*(\d+),\s*(\d+)%,\s*(\d+)%\s*\)", color).groups()
    r, g, b = colorsys.hls_to_rgb(int(h) / 360, int(l) / 100, int(s) / 100)
    return [round(255 * r), round(255 * g), round(255 * b)]
