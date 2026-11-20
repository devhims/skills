# codex-imagegen-cli

Generate images with **Codex's built-in image model** from the command line (`codex exec`), and save them into your project folder. Your agent writes the prompt, runs Codex, checks the result and redoes it if needed.

- **Text to image** in any aspect ratio (landscape, square, portrait 9:16)
- **Reference images**: keep a character or location and put it in a new scene, or combine two references into one image
- **Character turnaround sheets** and **transparent-background cutouts** with real alpha
- **No API key needed**: it uses your signed-in ChatGPT/Codex plan
- **Tested gotchas** covering prompt handling, real output sizes, style drift, draft vs final images and transparency checks

## Install

```bash
npx skills add devhims/skills --skill codex-imagegen-cli
```

## Requirements

- [Codex CLI](https://github.com/openai/codex), signed in: `npm i -g @openai/codex` (or `brew install codex`), then `codex login`
- `python3`, for the fallback image collector
- Optional: `ffmpeg`/`ffprobe`, to check sizes and transparency

> **Note:** every image uses your ChatGPT/Codex quota (roughly 12–25k tokens and 1–3 minutes per image). The skill tells the agent to ask before generating unless you asked for an image.

## Example

> "Generate a square gouache illustration of a fox drinking tea in a teahouse, then make a three-view turnaround sheet of the same fox on a transparent background."

## How it works

1. The agent writes a full prompt and runs `codex exec` with the prompt on stdin, passing any reference images with `-i`.
2. Codex generates the image with its built-in tool and copies the final image into your project folder.
3. If the copy didn't happen, [`scripts/collect_codex_images.py`](scripts/collect_codex_images.py) finds the image in Codex's output folder and copies it, including any drafts.
4. The agent checks the image against your request and references, and runs again with a precise fix if something is off.

The agent's full instructions are in [SKILL.md](SKILL.md).

---

[← All skills](../README.md) · [MIT License](../LICENSE)
