import argparse
import json

from icons import create_icons, icons_path
from preferences import create_preferences


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Create icons and preferences for A File Icon."
    )
    parser.add_argument(
        "-i", "--icons", action="store_true", help="convert svg icons to png"
    )
    parser.add_argument(
        "-p", "--preferences", action="store_true", help="create preferences"
    )

    with open(icons_path("icons.json")) as fp:
        icons = json.load(fp)

    options = parser.parse_args(argv)
    if not options.icons and not options.preferences:
        options.icons = True
        options.preferences = True

    if options.preferences:
        print("building preferences...")
        create_preferences(icons)

    if options.icons:
        print("building icons...")
        create_icons(icons)


if __name__ == "__main__":
    main()
