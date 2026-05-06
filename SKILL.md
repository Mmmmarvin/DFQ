---
name: hatch-pet-autowake
description: Create a Codex custom desktop pet from reference images or a text concept, install or rename the pet package, set it as the selected Codex pet, and configure a macOS LaunchAgent so the pet auto-wakes when Codex starts. Use when the user asks to generate/hatch a Codex pet and also wants it to persist, be renamed, copied/exported, or automatically appear after restarting Codex.
---

# Hatch Pet Autowake

## Overview

Use this skill to wrap the full custom-pet lifecycle: generate the pet with `$hatch-pet`, install it under `$CODEX_HOME/pets/<id>`, optionally rename it, set it as the selected Codex avatar, and add a small macOS helper that keeps the pet overlay open on Codex startup.

This skill composes the existing `hatch-pet` skill. Do not reimplement sprite generation here.

## User Inputs

Before starting a new pet, ask the user for:

- Pet display name, such as `小椰`.
- Short visual/personality description.
- Several reference images when available.

Reference images are strongly recommended. Ask for 3-6 images if the user has them:

- 1 clear front or three-quarter view.
- 1 side view if the pet has asymmetric markings, accessories, or a tail shape.
- 1-2 face/detail images for eyes, ears, markings, colors, or signature props.
- 1 image that captures the pet's personality or typical pose.

Explain why references matter: the generator must create one base image plus 9 animation rows. Without references, the base can still be made from text, but later rows are more likely to drift in face shape, markings, colors, body proportions, and accessories. Good references make the final spritesheet look like the same character across every state.

If the user has no references, continue from text, but tell them that identity consistency may be weaker and extra repair rounds may be needed.

## Animation States

Codex custom pets use a fixed `8 x 9` atlas. Each cell is `192 x 208` pixels. There are 9 animation states:

| Row | State | Frames | Current trigger or use |
| ---: | --- | ---: | --- |
| 0 | `idle` | 6 | Default resting state when there is no stronger activity state. Also used as the reduced-motion/static fallback. |
| 1 | `running-right` | 8 | Temporary drag state when the user moves the floating pet to the right. |
| 2 | `running-left` | 8 | Temporary drag state when the user moves the floating pet to the left. |
| 3 | `waving` | 4 | Reserved greeting/attention row. In the inspected Codex build, no automatic trigger was found, but the row is still part of the required atlas contract. |
| 4 | `jumping` | 5 | Temporary hover/interaction state when the pointer enters the pet. |
| 5 | `failed` | 8 | A blocked or failed notification, shown by Codex as a danger-level pet status. |
| 6 | `waiting` | 6 | A notification that needs user input, shown by Codex as a warning-level pet status. |
| 7 | `running` | 6 | Active work/loading state, shown while Codex is running or thinking. |
| 8 | `review` | 6 | Completed output ready to review, shown by Codex as a success-level pet status. |

Tell the user that all 9 states are generated even if some states are rare. The app expects the fixed atlas layout, and missing rows make the pet feel broken later.

## Workflow

1. **Collect references and expectations**
   - Ask for reference images using the guidance above.
   - Tell the user this pet needs 9 animation states and that generation may require one base image plus up to 9 row-strip jobs.
   - If the user wants to proceed without images, record that as an explicit text-only run.

2. **Generate or continue the pet**
   - Use `$hatch-pet` for all visual generation, row prompts, QA, validation, and packaging.
   - If the pet already exists, inspect `$CODEX_HOME/pets/<id>/pet.json` and the hatch run folder before changing anything.
   - Keep the `hatch-pet` visible checklist active during generation.

3. **Install or rename the package**
   - Use `scripts/set-pet-name.py` to normalize the folder id, display name, and description.
   - Prefer ASCII folder ids such as `xiaoye`; keep the user-facing display name in the requested language, such as `小椰`.
   - Preserve `spritesheet.webp`; do not regenerate images just to rename.

4. **Set the current selected pet**
   - The selected pet lives in `$CODEX_HOME/.codex-global-state.json` under:
     - `electron-persisted-atom-state.selected-avatar-id`
   - Custom pets use the value `custom:<pet-id>`.

5. **Enable auto-wake**
   - Use `scripts/install-autowake.py --pet-id <id>`.
   - On macOS, this installs:
     - `$CODEX_HOME/scripts/wake-<id>.sh`
     - `~/Library/LaunchAgents/com.codex.pet.<id>.autowake.plist`
   - The helper keeps the top-level `electron-avatar-overlay-open` field set to `true` and writes the `.bak` state file too. This matters because Codex may write the overlay closed on exit.

6. **Verify**
   - Confirm `pet.json`, `spritesheet.webp`, and `.codex-global-state.json` are consistent.
   - Confirm the LaunchAgent is loaded with `launchctl print gui/$(id -u)/com.codex.pet.<id>.autowake`.
   - If the user says the pet still does not appear, inspect window creation with a non-accessibility window list. The overlay can be open even if the user missed it visually.

## Commands

Rename/install selected pet:

```bash
python scripts/set-pet-name.py \
  --source-id milky \
  --pet-id xiaoye \
  --display-name "小椰" \
  --description "A cute cream and white British Shorthair cat companion named 小椰, with amber eyes."
```

Install auto-wake:

```bash
python scripts/install-autowake.py --pet-id xiaoye
```

Export a tidy desktop copy of generated images when requested:

```bash
python scripts/export-pet-images.py \
  --run-dir /absolute/path/to/hatch-run \
  --pet-id xiaoye \
  --output-dir "$HOME/Desktop/Xiaoye-pet-images"
```

## Notes

- This skill is macOS-focused for auto-wake because it uses LaunchAgents.
- Do not edit `/Applications/Codex.app`.
- Do not delete the original generated images under `$CODEX_HOME/generated_images`.
- If Codex is already running and the pet does not appear immediately, the helper should still prepare the state for the next app start. For current-session troubleshooting, inspect whether the overlay window exists before assuming failure.

## Reference

For animation row timing and trigger details, see `references/animation-states.md`.

For the original end-to-end run that inspired this skill, see `references/xiaoye-case-study.md`.
