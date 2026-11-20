# skills

Agent skills from my own development workflows: practical, tested, and refined through daily use. Each one started as something I kept doing by hand, then got tested on real projects, fixed where it broke, and written down so an agent can do it reliably. I add new ones as my workflows grow.

They work with Claude Code, Codex, Cursor, Kiro and other agents that support `SKILL.md` skills.

## Skills

| Skill | What it does |
|---|---|
| [codex-imagegen-cli](codex-imagegen-cli/) | Generate images with Codex's built-in image model, with reference images, turnaround sheets and transparent cutouts. No API key needed. |

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
