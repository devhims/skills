# skills

Agent skills from my own development workflows: practical, tested, and refined through daily use. Each one started as something I kept doing by hand, then got tested on real projects, fixed where it broke, and written down so an agent can do it reliably. I add new ones as my workflows grow.

They work with Claude Code, Codex, Cursor, Kiro and other agents that support `SKILL.md` skills.

## Skills

| Skill | What it does |
|---|---|
| [codex-imagegen-cli](codex-imagegen-cli/) | Generate images with the image tool built into OpenAI's Codex CLI, with reference images, parallel batches, turnaround sheets and transparent cutouts. Read-only sandbox, no API key needed. |

## Install

All skills:

```bash
npx skills add devhims/skills
```

One skill:

```bash
npx skills add devhims/skills --skill <skill-name>
```

## License

[MIT](LICENSE)
