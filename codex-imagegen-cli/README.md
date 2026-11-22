# codex-imagegen-cli

Generate images with the **`image_generation` tool built into OpenAI's [Codex CLI](https://github.com/openai/codex)**, run from the command line (`codex exec`) in a read-only sandbox, and save them into your project folder. Your agent writes the prompt, runs Codex, checks the result and redoes it if needed.

- **Text to image** in any aspect ratio (landscape, square, portrait 9:16)
- **Reference images**: keep a character or location and put it in a new scene, or combine two references into one image
- **Character turnaround sheets** and **transparent-background cutouts** with real alpha
- **No API key needed**: it uses your signed-in ChatGPT/Codex plan
- **Text in images**, with the agent checking the spelling
- **Tested gotchas** covering prompt handling, real output sizes, style drift, draft vs final images and transparency checks

## Install

```bash
npx skills add devhims/skills --skill codex-imagegen-cli
```

## Requirements

- [Codex CLI](https://github.com/openai/codex) (OpenAI's official CLI, published as `@openai/codex` on npm and `codex` on Homebrew), installed and signed in with `codex login`. Install it yourself from the official instructions; the skill never installs anything.
- `python3`, for the bundled image collector
- Optional: `ffmpeg`/`ffprobe`, to check sizes and transparency

> **Note:** every image uses your ChatGPT/Codex quota (roughly 9–25k tokens and 1–3 minutes per image). The skill tells the agent to ask before generating unless you asked for an image.

## Example

> "Generate a square gouache illustration of a fox drinking tea in a teahouse, then make a three-view turnaround sheet of the same fox on a transparent background."

## How it works

1. The agent writes the image description into a fixed prompt template that tells Codex to treat it as a picture description only, never as instructions.
2. It runs `codex exec --sandbox read-only` with the prompt on stdin, passing any reference images with `-i`. Codex generates the image with its built-in tool but can't write to your project or change anything.
3. [`scripts/collect_codex_images.py`](scripts/collect_codex_images.py) copies the image from that run's folder in `~/.codex/generated_images/` into your project, marking the final one if Codex made drafts. It's local only: no network, no commands.
4. The agent checks the image against your request and references, and runs again with a precise fix if something is off, asking you before a third attempt.

## Security

- Codex always runs with `--sandbox read-only`.
- The request is wrapped in `<image_request>` tags with an instruction not to follow anything inside them, and the agent never pastes in text from files, web pages or tool output.
- The skill never installs packages, signs in, or reads `~/.codex/auth.json`.

The agent's full instructions are in [SKILL.md](SKILL.md).

---

[← All skills](../README.md) · [MIT License](../LICENSE)
