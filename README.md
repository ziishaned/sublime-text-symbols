# Sublime Text Symbols

![Icons preview][img-preview]

File and folder icons for [Sublime Text](https://www.sublimetext.com/), powered by the
beautiful [Symbols][symbols] icon set by Miguel Solorio. Based on the
[A File Icon][a-file-icon] package.

## Highlights

* **160 file icons** from the Symbols icon set — languages, frameworks, config files and binaries.

* **Folder icons** for both the collapsed and expanded state, patched into any theme.

* Works with **every theme** — even with those, which don't provide file type icons.

* Displays file icons, even if the required syntax definition is not installed
  (hidden syntax aliases are generated on the fly for config files such as
  `tsconfig.json`, `.prettierrc` or `Dockerfile`).

* Optional single-color mode with custom color, opacity and size for all icons.

## Installation

The package is not published on Package Control. Install it directly from this
repository:

### Git clone

1. Open the `Packages` directory via menu item `Preferences → Browse Packages...`
2. Clone the repository into it. **The folder must be named `Sublime Text Symbols`**:

   ```bash
   git clone https://github.com/ziishaned/sublime-text-symbols.git "Sublime Text Symbols"
   ```

3. Restart Sublime Text.

### Download

1. [Download the `.zip`][download]
2. Unzip and rename the folder to `Sublime Text Symbols`
3. Copy the folder into your `Packages` directory
4. Restart Sublime Text

> **Note:** If the official `A File Icon` package is installed via Package
> Control, remove it first to avoid conflicts.

## Customization

You can change the color, opacity level and size of the icons by modifying your
user preferences file, which you can find by:

* `Preferences → Package Settings → Sublime Text Symbols → Settings`
* Choose `Preferences: Sublime Text Symbols Settings` in the `Command Palette`

The most important options:

| Option | Description |
| ------ | ----------- |
| `color` | Tint all icons (including folders) with a single color, e.g. `"#8899AA"` |
| `opacity` | The opacity level of the default icon state |
| `size` | The icon size (defaults to `8`) |
| `aliases` | Set `false` to apply icons to installed syntaxes only |
| `force_mode` | Use these icons even if your theme provides its own |

## Folder icons

The folder icons are applied by generating `.sublime-theme` patches for all
installed themes. Just like in VS Code, the Symbols icon set uses the **same
artwork for collapsed and expanded folders** — the state is indicated by the
disclosure arrows next to the folder.

## Wrong icons

Sublime Text uses syntax scopes for file-specific icons. That's why icons of
syntax definitions provided by the community require them to be installed.

See the list of [community packages][packages] you may need to install to see
the right icon.

## Troubleshooting

If something goes wrong try to:

1. Open `Command Palette` using menu item `Tools → Command Palette...`
2. Choose `Sublime Text Symbols: Revert to a Freshly Installed State`
3. Restart Sublime Text

## Icon mapping

This package was created by re-mapping the original A File Icon set to the
Symbols icon set:

* 147 icons were replaced by their Symbols equivalent
* 115 icons without an equivalent were removed
* 15 icons were added (`deno`, `prettier`, `vitest`, `tsconfig`, `tauri`,
  `firebase`, `gitlab`, `cypress`, `rescript`, `gdscript`, `gdproject`, `luau`,
  `cucumber`, `exe`, `readme`)

Notable substitutions, following the associations of the Symbols theme:
`css` → brackets, `json` → brackets, `html` → code, `scss` → sass,
`sql` → database, `xlsx` → spreadsheet, `.ps1`/`.bat` → shell,
`.sln` → visual studio, `.erb` → ruby, `wgsl` → webgpu and
`diff`/`patch` → patch.

## How it works

In simple terms, the package does the following:

1. Copies all the necessary files right after install or upgrade to a hidden
   `zzz Sublime Text Symbols` overlay package, which is loaded as late as possible
2. Searches all installed themes
3. Patches them by generating `<theme-name>.sublime-theme` files, which
   override the file type and folder icon definitions
4. Creates hidden syntax aliases for files without an installed syntax

The real process is just a little bit more complex to minimize hard drive I/O.

## Building from source

The SVG sources are converted to `@1x`, `@2x` and `@3x` PNG assets by a python
build script. It requires [cairo](https://www.cairographics.org/)
(e.g. `brew install cairo` on macOS):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python build           # icons + preferences
.venv/bin/python build --icons   # icons only
```

## Acknowledgments

* [A File Icon][a-file-icon] by Ihor Oleksandrov and DeathAxe — the package
  this project is based on (MIT License)
* [Symbols for VS Code][symbols] by Miguel Solorio — the icon set (MIT License)

## License

[MIT](LICENSE.md)

<!-- Links -->

[a-file-icon]: https://github.com/SublimeText/AFileIcon
[symbols]: https://github.com/miguelsolorio/vscode-symbols
[packages]: PACKAGES.md
[download]: https://github.com/ziishaned/sublime-text-symbols/archive/refs/heads/main.zip

<!-- Assets -->

[img-preview]: media/preview.png
