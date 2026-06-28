# twemoji-colr

Build a COLR/CPAL color OpenType font from the [Twemoji](https://github.com/jdecked/twemoji) emoji image collection.

This project currently provides **COLR/CPAL v0 only**.

The resulting font is usable only on systems that support layered color TrueType fonts, such as Windows 8.1 and later, plus Firefox and other Gecko-based applications.

| COLR/CPAL | Windows                                                    | Chrome / Blink | Firefox / Gecko | Safari / WebKit |
| :-------: | :--------------------------------------------------------- | :------------: | :-------------: | :-------------: |
|    v0     | Windows 8.1 6.3.9600.16384                                 |       71       |       32        |       11        |
|    v1     | Windows 11 22H2 22621.2715<br />Windows 11 23H2 22631.2715 |       98       |       107       |                 |

Systems without compatible color-font support may display blank glyphs.

## Getting started

This repository is a Python CLI tool built on top of [nanoemoji](https://github.com/googlefonts/nanoemoji) and [fonttools](https://github.com/fonttools/fonttools).

Requirements:

- [uv](https://docs.astral.sh/uv/) (includes Python/runtime management)
- Internet access for downloading Twemoji source archives from GitHub

Create an environment and install dependencies:

```bash
uv sync --locked
```

## Build

Build from the latest Twemoji tag:

```bash
uv run python -m twemoji_font_forge
```

Build from a specific tag:

```bash
uv run python -m twemoji_font_forge --tag v14.0.0
```

Force a rebuild even if outputs already exist:

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

The generated font version is derived from the tag after removing the `v` prefix.
For example, `v14.0.0` becomes font version `14.0`.
