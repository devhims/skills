---
name: codex-imagegen-cli
description: Generate raster images with Codex's built-in image model from the command line (codex exec), with optional reference images, and save them into the project folder. Use for codex image gen, AI text-to-image, reference-image edits and restyles, character turnaround sheets, location plates, storyboard frames, and transparent-background cutouts.
license: MIT
---

# codex-imagegen-cli

Generate images by running the Codex CLI's built-in image tool from your
shell. Codex uses the user's ChatGPT/Codex plan, so no `OPENAI_API_KEY` is
needed.

## When to use

- The user wants a real AI-generated raster image (painterly, photographic,
  textured craft, character sheets, location plates, storyboard frames), not
  vector or code-drawn art.
- No other image generation tool is available in this environment, or the
  user asked for Codex specifically.
- You need image-to-image work: keep a character or layout from a reference
  image and restyle, extend or re-pose it.

Each image spends the user's Codex quota. Unless the user asked for
Codex/AI image generation, ask before running it.

## Requirements

- The Codex CLI, signed in (`codex login`; `~/.codex/` or `$CODEX_HOME` exists).
  Install it with `npm i -g @openai/codex` or `brew install codex`. On macOS
  the ChatGPT desktop app also ships one at
  `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`.
- `python3` for the fallback helper. `ffmpeg`/`ffprobe` are optional, for
  checking image sizes and transparency.

## Steps

1. **Find the CLI.** Try `codex` on PATH first, then the ChatGPT.app path
   above. Confirm with `codex --version`, then check that
   `codex features list | grep image_generation` shows `stable true`.
   Never read `~/.codex/auth.json`.
2. **Write the prompt.** Describe the whole image: subject, views, style,
   material, lighting, background, and "No text or labels" when wanted.
   State the aspect ratio in words ("portrait 9:16", "square"). Start with an
   explicit line: "Use your built-in image generation tool (not code, not
   SVG)". Otherwise Codex may draw the image with code. Codex also adds
   unrequested props (an extra plate of food, for example). When the scene
   must match a storyboard or plate, add "Nothing else in the scene
   besides …".
3. **Run Codex yourself** in the shell, with the prompt on stdin, and save
   its output to a log. `<dir>` is the user's project folder where the image
   should end up. End the prompt with a copy line: "After generating, copy
   the final image to <dir>/<stem>.png with a shell command, then confirm it
   with ls -l."
   `echo "<prompt>" | codex exec --skip-git-repo-check --sandbox workspace-write -C <dir> [-i ref1.png -i ref2.png] - 2>&1 | tee <dir>/<stem>.codex.log`
   `workspace-write` lets Codex write only inside `-C <dir>` and `/tmp`, so
   `-C` must be the destination folder. Give it a long timeout (about 10
   minutes). Each image takes 1–3 minutes.
4. **Confirm the image landed.** Check that `<dir>/<stem>.png` exists and is
   the image Codex's reply calls final. If it is missing (sandbox failed,
   copy skipped, `read-only` used), collect it with the helper in this
   skill's folder (the folder that holds this SKILL.md). Use its absolute
   path, so no `cd` is needed:
   `python3 <skill-dir>/scripts/collect_codex_images.py --log <dir>/<stem>.codex.log --out <dir> --name <stem>`
   The helper also recovers drafts. It reads the `session id:` from the log
   and copies every PNG from `$CODEX_HOME/generated_images/<session-id>/`
   (default `~/.codex/...`) to `<dir>/<stem>.png` (or `<stem>-N.png`), then
   prints the paths. Codex often checks its own image (aspect ratio, a prop
   carried over from a reference) and generates again, so one run can leave
   2 PNGs. In that case the helper writes `final: <path>` to stderr. Use that
   one; the others are drafts. Without the helper, copy the last PNG path
   named in Codex's reply.
5. **Check the result yourself.** Open the PNG and compare it with the
   references: identity markers, colours, view count, aspect ratio, any
   stray text, and any props you didn't ask for. Fix it with a new run that
   names the fault plainly. Pass the last good output with `-i` so identity
   carries forward.
6. **Batch carefully.** Run one image per call, one call at a time. Record
   the prompt, the refs and the output path for each image (for example in
   a JSON next to the images) so you can redo any of them.

## Gotchas

- **`-i` swallows the prompt.** `-i/--image` takes many values, so a
  positional prompt after it is read as another file. Codex then says "No
  prompt provided via stdin". Always pass the prompt on stdin with a final `-`.
- **Sizes are not fixed.** The default is 1536×1024 landscape. Measured
  results: "landscape 3:2" gave 1536×1024, "square" 1254×1254, and
  "portrait 9:16" 1060×1484 (5:7) on the first try, then 941×1672 after Codex
  retried. Read the real size before fitting the image into a frame (macOS:
  `sips -g pixelWidth -g pixelHeight f.png`; anywhere:
  `ffprobe -v error -show_entries stream=width,height f.png`).
- **Images are saved under `$CODEX_HOME/generated_images/<session-id>/` first.**
  Each `codex exec` call is a new session with its own folder. With
  `--sandbox workspace-write` and a copy line in the prompt, Codex copies the
  final image into `-C <dir>` itself. In testing it ran `cp -n`, `ls -l` and
  `cmp`. Some setups see the sandbox fail to start
  (`node_repl/js (failed)`). If the log shows that, or the file is missing,
  use the helper from step 4. Generation works even then, and
  `--sandbox read-only` is enough for generation alone. Codex's `cp -n`
  won't overwrite an existing file, so use a new stem or delete the old file
  first.
- **Codex reads its own imagegen skill first.** It cats
  `~/.codex/skills/.system/imagegen/SKILL.md` (about 300 log lines) before
  generating. This is normal and is part of the token cost. That skill
  prefers the built-in `image_gen` tool. Its fallback, `scripts/image_gen.py`,
  needs `OPENAI_API_KEY`. A run that tries that script or asks for an API key
  has failed, so don't accept it. Check the built-in tool with
  `codex features list` and run again.
- **It costs quota.** About 12–25k tokens per call on the user's ChatGPT/Codex
  plan. Calls with references or a Codex retry use the most. Each call takes
  about 1–3 minutes (45–130 s seen).
- **References guide, they don't lock.** Both coded/vector references and
  generated ones keep the layout and the identity markers well. Still check
  fine details like button count, handedness and scarf side on every image.
- **Several references work.** Pass `-i a.png -i b.png` and name them in the
  prompt by order ("Image 1 is the character, image 2 is the location").
  A character reference plus a location reference gave one scene that kept
  both.
- **Style can drift.** A character sheet on a transparent background turned
  a gouache character into a plush/3D render. A run that fixed it did three
  things. It passed the original style image first, as "Image 1 is the style
  master". It described the technique ("opaque gouache on paper, flat matte
  colour shapes, visible brush strokes, dry-brush edges, no smooth
  gradients"). It also listed what to avoid ("Do NOT make it 3D, CGI, a plush
  toy, felt, rendered fur; no glossy highlights, no subsurface glow").
- **Transparent backgrounds are real alpha.** Ask for "Transparent background
  (real alpha, no checkerboard)". Hidden colour stays under the transparent
  pixels, and an image viewer that ignores alpha shows it as a coloured
  glow. Flatten onto white before you judge the image:
  `ffmpeg -f lavfi -i color=white:s=WxH -i in.png -filter_complex overlay -frames:v 1 check.png`.
  The opaque parts come out at alpha 253–254, not 255.
- **No text in images.** Ask for "no text or labels" and add any labels
  yourself in an HTML or SVG wrapper. Generated lettering is unreliable.
- **Paths.** Pass absolute paths for reference images (`-i`) and the helper's
  `--out`, because `-C` changes Codex's working directory.
