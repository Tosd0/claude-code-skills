# Claude Code Skills

A collection of open-source skills for [Claude Code](https://claude.com/claude-code).

## Quick Start

Copy the following to your AI assistant:

```
请阅读 https://github.com/lldxflwb/claude-code-skills 帮我安装里面的 skills
```

## Skills

| Skill | Description |
|-------|-------------|
| [codex](skills/codex/) | Invoke Codex CLI from Claude Code to get a second opinion from GPT models. Supports session resume for multi-turn conversations. |
| [tikz](skills/tikz/) | TikZ diagram rendering with HTTP preview server. Write TikZ code, compile to SVG, view in browser. Includes a plan viewer with e-ink reading mode and pagination. |

## Installation

Copy or symlink the skill directory to your Claude Code skills folder:

```bash
# Install a single skill (symlink recommended)
ln -s /path/to/skills/codex ~/.claude/skills/codex
ln -s /path/to/skills/tikz ~/.claude/skills/tikz
```

After installing, check each skill's `setup.md` for dependencies and install them:

```bash
# tikz skill dependencies (macOS)
which tectonic || brew install tectonic
which pdf2svg || brew install pdf2svg

# codex skill dependencies
which codex || npm install -g @anthropic-ai/codex
```

## Contributing

1. Each skill lives in its own directory under `skills/`
2. Every skill must have a `SKILL.md` with proper frontmatter
3. Supporting scripts go in a `scripts/` subdirectory
4. Include clear prerequisites and usage examples

## License

MIT
