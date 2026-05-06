# Animation States

Codex custom pets use one fixed spritesheet atlas:

- 8 columns x 9 rows.
- 192 x 208 pixels per cell.
- Unused cells must be transparent.
- All 9 rows should exist, even when a row is rarely triggered.

| Row | State | Frames | Timing | Trigger or use |
| ---: | --- | ---: | --- | --- |
| 0 | `idle` | 6 | 280, 110, 110, 140, 140, 320 ms | Default resting state when there is no stronger activity state. The first frame is also used for reduced motion. |
| 1 | `running-right` | 8 | 120 ms each, final 220 ms | Temporary drag state when the floating pet is moved to the right. |
| 2 | `running-left` | 8 | 120 ms each, final 220 ms | Temporary drag state when the floating pet is moved to the left. |
| 3 | `waving` | 4 | 140 ms each, final 280 ms | Reserved greeting or attention state. No automatic trigger was found in the inspected Codex build, but the atlas row is required. |
| 4 | `jumping` | 5 | 140 ms each, final 280 ms | Temporary pointer-hover or direct-interaction state. |
| 5 | `failed` | 8 | 140 ms each, final 240 ms | Blocked or failed notification, mapped from a danger-level Codex status. |
| 6 | `waiting` | 6 | 150 ms each, final 260 ms | Codex needs user input, mapped from a warning-level Codex status. |
| 7 | `running` | 6 | 120 ms each, final 220 ms | Codex is running, thinking, or calling tools, mapped from a loading status. |
| 8 | `review` | 6 | 150 ms each, final 280 ms | Completed output is ready to review, mapped from a success-level Codex status. |

## Prompting Notes

- Keep every row visually consistent with the canonical base image and user references.
- Directional rows should read clearly left or right.
- `running-left` may be mirrored from `running-right` only when the design is symmetric enough that mirroring does not break markings, accessories, handed props, lighting, or readable details.
- `waving` should show the gesture through the paw or body pose only; avoid loose wave marks or symbols.
- `jumping` should show body position and anticipation; avoid detached shadows, dust, or impact marks.
- `failed` may use attached tears, small smoke puffs, or attached stars when they stay inside the sprite silhouette; avoid detached symbols.
- `review` should read as focused or thoughtful through posture, eyes, blink, or head tilt; avoid adding UI, papers, code, or magnifying glasses unless already part of the pet identity.
