# Hatch Pet Autowake

Create a Codex custom desktop pet from reference images, install it, rename it, and make it auto-wake when Codex starts.

This skill was extracted from the end-to-end creation of a custom pet named `小椰`: generation, packaging, image export, pet renaming, selecting the custom pet, and fixing startup auto-wake on macOS.

## What It Does

- Guides the user to upload useful pet reference images.
- Generates the pet through the existing Codex `$hatch-pet` workflow.
- Installs or renames the final pet package under `$CODEX_HOME/pets/<id>`.
- Sets the pet as the selected Codex avatar.
- Installs a macOS LaunchAgent that keeps the Codex pet overlay open after app restarts.
- Exports a tidy copy of generated pet images when requested.

## Recommended References

Ask users to provide 3-6 reference images when possible:

- A clear front or three-quarter view.
- A side view, especially for asymmetric markings or accessories.
- Face/detail images for eyes, ears, markings, palette, or props.
- A pose or personality image.

References are important because the pet is not a single picture. Codex needs a base image plus 9 animation rows. Good references keep the face, colors, silhouette, markings, and props consistent across every row.

Text-only generation is possible, but identity drift is more likely and repair rounds may be needed.

## Animation States

Codex pets use a fixed `8 x 9` spritesheet. Each cell is `192 x 208` pixels. The 9 rows are:

| Row | State | Frames | Trigger or use |
| ---: | --- | ---: | --- |
| 0 | `idle` | 6 | Default resting state and reduced-motion fallback. |
| 1 | `running-right` | 8 | Dragging the floating pet to the right. |
| 2 | `running-left` | 8 | Dragging the floating pet to the left. |
| 3 | `waving` | 4 | Reserved greeting/attention row; no automatic trigger was found in the inspected Codex build. |
| 4 | `jumping` | 5 | Pointer hover or direct interaction with the pet. |
| 5 | `failed` | 8 | Blocked or failed notification. |
| 6 | `waiting` | 6 | Codex needs user input. |
| 7 | `running` | 6 | Codex is running, thinking, or calling tools. |
| 8 | `review` | 6 | Completed output is ready to review. |

All rows should still be generated because the app expects the fixed atlas layout.

## Install From GitHub

Install it with Codex's skill installer from the GitHub skill path:

```text
$skill-installer install from https://github.com/Mmmmarvin/DFQ/tree/main/hatch-pet-autowake
```

Restart Codex after installing new skills.

Installing this skill only teaches Codex the workflow. It does not immediately create a pet or enable auto-wake. After restart, run the skill with a request like:

```text
$hatch-pet-autowake Create a custom Codex pet from my reference images, install it, and make it auto-wake when Codex starts.
```

Auto-wake is configured after a pet package exists, because the helper needs the installed pet id.

## Files

- `SKILL.md`: the Codex skill instructions.
- `agents/openai.yaml`: user-facing skill metadata.
- `scripts/set-pet-name.py`: rename or normalize an installed custom pet and select it.
- `scripts/install-autowake.py`: install the macOS auto-wake helper.
- `scripts/export-pet-images.py`: collect generated images and installed pet files into a tidy export folder.
- `references/animation-states.md`: detailed row, timing, and trigger notes.
- `references/xiaoye-case-study.md`: implementation notes from the original pet.

## Notes

Auto-wake is macOS-focused because it uses LaunchAgents. The generation workflow depends on Codex's existing `$hatch-pet` and `$imagegen` skills.
