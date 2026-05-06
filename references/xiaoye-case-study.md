# Xiaoye Case Study

This reference records the practical workflow used for a custom cream-and-white British Shorthair Codex pet.

## Pet Generation

- Pet started as `Milky`, generated with `$hatch-pet` from four cat reference images.
- The hatch run created `base`, row strips, extracted frames, final spritesheet, contact sheet, validation JSON, and preview videos.
- Some subagents disconnected, so remaining rows were completed sequentially in the parent thread after user approval.
- Final package was written to `$CODEX_HOME/pets/milky`.

## Rename

The pet was renamed from `milky` to `xiaoye`:

```json
{
  "id": "xiaoye",
  "displayName": "小椰",
  "description": "A cute cream and white British Shorthair cat companion named 小椰, with amber eyes.",
  "spritesheetPath": "spritesheet.webp"
}
```

## Autowake Findings

Codex uses two different state locations:

- Current selected custom pet:
  `electron-persisted-atom-state.selected-avatar-id = "custom:xiaoye"`
- Overlay open flag:
  top-level `electron-avatar-overlay-open = true`

Do not put `electron-avatar-overlay-open` only inside `electron-persisted-atom-state`; Codex reads the top-level field for startup restore.

Codex may write the overlay state back to `false` on exit. A LaunchAgent that runs every second and writes both `.codex-global-state.json` and `.codex-global-state.json.bak` prevents a restart race.

## Window Check

On macOS, if the user cannot see the pet, the overlay may still exist. A CoreGraphics window list can show a Codex window around `356 x 320` on layer `3`, which is the avatar overlay. This check does not require Accessibility permission.
