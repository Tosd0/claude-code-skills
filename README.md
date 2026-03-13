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

## Installation

Copy the skill directory to your Claude Code skills folder:

```bash
# Install a single skill
cp -r skills/codex ~/.claude/skills/codex
```

## Prerequisites

Each skill may have its own prerequisites. Check the `SKILL.md` file in each skill directory for details.

## Contributing

1. Each skill lives in its own directory under `skills/`
2. Every skill must have a `SKILL.md` with proper frontmatter
3. Supporting scripts go in a `scripts/` subdirectory
4. Include clear prerequisites and usage examples

## License

MIT
