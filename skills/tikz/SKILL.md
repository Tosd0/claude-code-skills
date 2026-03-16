---
name: tikz
description: "Use TikZ to create high-quality vector diagrams and visualizations rendered to SVG with instant browser preview. Use this skill whenever the user asks to draw, visualize, or create diagrams — flowcharts, architecture diagrams, neural networks, mathematical figures, circuit diagrams, graphs, trees, state machines, timelines, or any structured visual. Also triggers on mentions of TikZ, LaTeX drawing, or pgfplots. Even if the user just says 'draw me a diagram' without mentioning TikZ, use this skill if TikZ is a good fit."
user-invocable: true
argument-hint: "<description of the diagram to create>"
---

# TikZ Diagram Skill

## How to Use

Two steps:

**Step 1.** Write a `.tex` file in the project directory using the Write tool:

```latex
\usetikzlibrary{arrows.meta, positioning}
\begin{tikzpicture}
  \node[circle, draw] (a) {A};
  \node[circle, draw, right=of a] (b) {B};
  \draw[->] (a) -- (b);
\end{tikzpicture}
```

**Step 2.** Pass the file path to the render script:

```bash
python3 /Users/karlchen/.claude/skills/tikz/scripts/render_tikz.py <path-to-tex-file>
```

Output is one line: the URL. Each render gets a unique timestamp, so re-running the same file produces a new URL. Return the URL to the user. Done.

**Do NOT:**
- Call `ensure_server.py` — the render script handles server internally
- Open the URL with `open` command or browser tools
- Try to preview or read the SVG file

## TikZ Tips

- Write partial code (just `\begin{tikzpicture}...\end{tikzpicture}` + `\usetikzlibrary` / `\usepackage` lines) — auto-wrapped in `standalone` document
- Or write a full document with `\documentclass` — used as-is
- Use `positioning` library for `right=of` syntax
- Use `arrows.meta` for modern arrow styles

## Error Recovery

Compilation errors are printed to stderr. Read the error, fix the `.tex` file, re-render.

## Prerequisites

Before first use, check and install dependencies:

```bash
which tectonic || brew install tectonic
which pdf2svg || brew install pdf2svg
```

If `brew` is behind a proxy, use the user's proxy alias (e.g. `pbrew`). See [setup.md](setup.md) for details.

## Server Management

Server runs automatically. To stop (only when user explicitly asks):

```bash
python3 /Users/karlchen/.claude/skills/tikz/scripts/ensure_server.py --stop
```
