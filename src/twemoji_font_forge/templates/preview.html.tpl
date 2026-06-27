<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Twemoji Font Preview</title>
    <style>
      @font-face {
        font-family: "TwemojiPreview";
        src: url("$font_file_name") format("truetype");
        font-display: swap;
      }

      :root {
        --bg: #f6f3ea;
        --card: #fffdf8;
        --ink: #1f2a37;
        --accent: #0f766e;
        --line: #d9d5c8;
      }

      body {
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        background: radial-gradient(
          circle at 10% 0%,
          #fff7da 0%,
          var(--bg) 45%,
          #ece8dd 100%
        );
        color: var(--ink);
      }

      .wrap {
        max-width: 1200px;
        margin: 0 auto;
        padding: 28px 16px 48px;
      }

      h1 {
        margin: 0 0 8px;
        font-size: 28px;
        letter-spacing: 0.2px;
      }

      .meta {
        margin: 0 0 18px;
        color: #4b5563;
        font-size: 14px;
      }

      .section {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 14px;
        box-shadow: 0 8px 28px rgba(25, 35, 45, 0.06);
      }

      .range-title {
        margin: 0 0 10px;
        font-size: 14px;
        color: #374151;
        font-family: Consolas, "Courier New", monospace;
      }

      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(74px, 1fr));
        gap: 8px;
      }

      .cell {
        border: 1px solid var(--line);
        border-radius: 10px;
        padding: 8px 6px;
        text-align: center;
        background: #fff;
      }

      .glyph {
        font-family: "TwemojiPreview", serif;
        font-size: 26px;
        line-height: 1.2;
        min-height: 32px;
      }

      .cp {
        margin-top: 4px;
        font-size: 11px;
        color: #6b7280;
        font-family: Consolas, "Courier New", monospace;
      }

      .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        background: color-mix(in srgb, var(--accent) 14%, white);
        color: #0b5f58;
        font-size: 12px;
        margin-left: 8px;
      }

      .tabs {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 12px;
      }

      .tab {
        border: 1px solid var(--line);
        background: #fff;
        color: #374151;
        border-radius: 999px;
        font-size: 13px;
        padding: 6px 12px;
        cursor: pointer;
      }

      .tab.active {
        background: color-mix(in srgb, var(--accent) 14%, white);
        border-color: color-mix(in srgb, var(--accent) 35%, var(--line));
        color: #0b5f58;
      }

      .panel[hidden] {
        display: none;
      }

      .grid-seq {
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      }

      .cell-seq {
        padding: 10px 8px;
      }

      .cell-seq .glyph {
        font-size: 30px;
      }

      .cp {
        margin-top: 4px;
        font-size: 11px;
        color: #6b7280;
        font-family: Consolas, "Courier New", monospace;
        white-space: normal;
        overflow-wrap: anywhere;
        word-break: break-word;
        line-height: 1.35;
      }

      @media (max-width: 640px) {
        .grid-seq {
          grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        }
      }
    </style>
  </head>
  <body>
    <div class="wrap">
      <h1>Twemoji Font Preview</h1>
      <p class="meta">
        Font file: <strong>$font_file_name</strong>
        <span class="badge">Code points from TTF cmap</span>
      </p>
      <div id="root"></div>
    </div>

    <script>
      const ranges = $ranges_json;
      const sequences = $sequences_json;
      const root = document.getElementById("root");

      const hex = (n) => "U+" + n.toString(16).toUpperCase().padStart(4, "0");

      const tabs = document.createElement("div");
      tabs.className = "tabs";

      const codeTab = document.createElement("button");
      codeTab.className = "tab active";
      codeTab.textContent = "Code points";

      const seqTab = document.createElement("button");
      seqTab.className = "tab";
      seqTab.textContent = "GSUB sequences";
      seqTab.disabled = !sequences.length;

      tabs.appendChild(codeTab);
      tabs.appendChild(seqTab);
      root.appendChild(tabs);

      const codePanel = document.createElement("div");
      codePanel.className = "panel";

      const seqPanel = document.createElement("div");
      seqPanel.className = "panel";
      seqPanel.hidden = true;

      const switchTab = (showSequences) => {
        codePanel.hidden = showSequences;
        seqPanel.hidden = !showSequences;
        codeTab.classList.toggle("active", !showSequences);
        seqTab.classList.toggle("active", showSequences);
      };

      codeTab.addEventListener("click", () => switchTab(false));
      seqTab.addEventListener("click", () => {
        if (!seqTab.disabled) {
          switchTab(true);
        }
      });

      if (sequences.length) {
        const section = document.createElement("section");
        section.className = "section";

        const title = document.createElement("h2");
        title.className = "range-title";
        title.textContent = "GSUB sequences (" + sequences.length + " glyphs)";
        section.appendChild(title);

        const grid = document.createElement("div");
        grid.className = "grid grid-seq";

        for (const seq of sequences) {
          const cell = document.createElement("div");
          cell.className = "cell cell-seq";

          const glyph = document.createElement("div");
          glyph.className = "glyph";
          glyph.textContent = String.fromCodePoint(...seq);

          const code = document.createElement("div");
          code.className = "cp";
          code.textContent = seq.map(hex).join(" ");

          cell.appendChild(glyph);
          cell.appendChild(code);
          grid.appendChild(cell);
        }

        section.appendChild(grid);
        seqPanel.appendChild(section);
      }

      for (const [start, end] of ranges) {
        const section = document.createElement("section");
        section.className = "section";

        const title = document.createElement("h2");
        title.className = "range-title";
        title.textContent =
          hex(start) +
          " .. " +
          hex(end) +
          " (" +
          (end - start + 1) +
          " glyphs)";
        section.appendChild(title);

        const grid = document.createElement("div");
        grid.className = "grid";

        for (let cp = start; cp <= end; cp++) {
          const cell = document.createElement("div");
          cell.className = "cell";

          const glyph = document.createElement("div");
          glyph.className = "glyph";
          glyph.textContent = String.fromCodePoint(cp);

          const code = document.createElement("div");
          code.className = "cp";
          code.textContent = hex(cp);

          cell.appendChild(glyph);
          cell.appendChild(code);
          grid.appendChild(cell);
        }

        section.appendChild(grid);
        codePanel.appendChild(section);
      }

      root.appendChild(codePanel);
      root.appendChild(seqPanel);
    </script>
  </body>
</html>
