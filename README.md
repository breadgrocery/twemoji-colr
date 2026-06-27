# twemoji-colr

Project to create a COLR/CPAL-based color OpenType font
from the [Twemoji](https://github.com/jdecked/twemoji) collection of emoji images.

Note that the resulting font will **only** be useful on systems that support
layered color TrueType fonts; this includes Windows 8.1 and later,
as well as Mozilla Firefox and other Gecko-based applications running on
any platform.

Systems that do not support such color fonts will show blank glyphs
if they try to use this font.

## Getting started

This project is now a Python CLI tool built on top of
[nanoemoji](https://github.com/googlefonts/nanoemoji) and
[fonttools](https://github.com/fonttools/fonttools).

Requirements:

- [uv](https://docs.astral.sh/uv/) (includes Python/runtime management)
- Internet access for downloading Twemoji source archives from GitHub

Create an environment and install dependencies:

```bash
uv sync --locked
```

## Build

Build with the latest Twemoji tag:

```bash
uv run python -m twemoji_font_forge
```

Build a specific tag:

```bash
uv run python -m twemoji_font_forge --tag v14.0.0
```

Force rebuild even if output exists:

```bash
uv run python -m twemoji_font_forge --tag v14.0.0 --force
```

You can also run via module mode:

```bash
uv run python -m twemoji_font_forge run --tag v14.0.0
```

## CLI options

```text
twemoji_font_forge run [OPTIONS]

--repo TEXT      Twemoji repository in owner/name format (default: jdecked/twemoji)
--tag TEXT       Twemoji tag to build (default: latest tag)
--output PATH    Output directory (default: dist)
--workdir PATH   Build/cache directory (default: .build)
--force          Force rebuild even when output already exists
```

## Output

For a given tag (for example `v14.0.0`), outputs are written to:

- `dist/v14.0.0/Twemoji.ttf`
- `dist/v14.0.0/preview.html`

The generated font version is derived from the tag with the `v` prefix removed.
For example, `v14.0.0` becomes font version `14.0`.
