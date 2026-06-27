from __future__ import annotations

import json
from pathlib import Path

from fontTools.ttLib import TTFont

from .templates import render_preview_html


def _codepoint_ranges(codepoints: list[int]) -> list[tuple[int, int]]:
    if not codepoints:
        return []

    ranges: list[tuple[int, int]] = []
    start = codepoints[0]
    end = codepoints[0]

    for value in codepoints[1:]:
        if value == end + 1:
            end = value
        else:
            ranges.append((start, end))
            start = value
            end = value

    ranges.append((start, end))
    return ranges


def _collect_cmap_codepoints(ttf_file: Path) -> list[int]:
    with TTFont(ttf_file) as font:
        cmap = font.getBestCmap() or {}
    return sorted(cmap.keys())


def _collect_gsub_sequences(ttf_file: Path) -> list[tuple[int, ...]]:
    with TTFont(ttf_file) as font:
        cmap = font.getBestCmap() or {}
        reverse_cmap: dict[str, int] = {}
        for codepoint, glyph_name in cmap.items():
            reverse_cmap.setdefault(glyph_name, codepoint)

        if "GSUB" not in font:
            return []

        lookup_list = font["GSUB"].table.LookupList
        if lookup_list is None:
            return []

        sequences: set[tuple[int, ...]] = set()
        for lookup in lookup_list.Lookup:
            if lookup.LookupType != 4:
                continue
            for subtable in lookup.SubTable:
                ligatures = getattr(subtable, "ligatures", None)
                if not ligatures:
                    continue

                for first_glyph, ligature_list in ligatures.items():
                    for ligature in ligature_list:
                        glyph_sequence = [first_glyph, *ligature.Component]
                        codepoint_sequence: list[int] = []
                        for glyph_name in glyph_sequence:
                            codepoint = reverse_cmap.get(glyph_name)
                            if codepoint is None:
                                codepoint_sequence = []
                                break
                            codepoint_sequence.append(codepoint)

                        if len(codepoint_sequence) >= 2:
                            sequences.add(tuple(codepoint_sequence))

    return sorted(sequences)


def generate_preview_html(ttf_file: Path) -> Path:
    codepoints = _collect_cmap_codepoints(ttf_file)
    ranges = _codepoint_ranges(codepoints)
    ranges_json = json.dumps([[start, end] for start, end in ranges])
    sequences = _collect_gsub_sequences(ttf_file)
    sequences_json = json.dumps([list(sequence) for sequence in sequences])
    html_file = ttf_file.with_name("preview.html")
    html = render_preview_html(ttf_file.name, ranges_json, sequences_json)
    html_file.write_text(html, encoding="utf-8")
    return html_file
