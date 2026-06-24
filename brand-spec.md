# Brand Specification - Where Is AI Going?

## Color Palette (OKLch)
- `--bg`: `oklch(98.5% 0.003 240)` (Very light cool grey / off-white background)
- `--surface`: `oklch(100% 0 0)` (Pure white surface)
- `--surface-hover`: `oklch(97% 0.004 240)` (Slightly darker grey for hover states)
- `--fg`: `oklch(15% 0.015 250)` (Dark charcoal text color)
- `--muted`: `oklch(52% 0.012 250)` (Muted grey for descriptions and metadata)
- `--border`: `oklch(90.5% 0.006 250)` (Subtle delicate grey border)
- `--accent`: `oklch(58% 0.18 255)` (Electric Blue-Cyan for active tags, progress bars, and accent states)
- `--highlight`: `oklch(62% 0.22 25)` (Vibrant Red/Coral for highlighted node border, matching the drawing's dashed outline)

## Typography Mood
- **Display Font Stack**: `-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', 'PingFang SC', sans-serif`
- **Body Font Stack**: `-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', 'PingFang SC', sans-serif`
- **Mono Font Stack**: `'JetBrains Mono', 'IBM Plex Mono', Menlo, monospace` (for metadata, node tags, and scores)

## Layout & Posture Rules
1. **Pill-style Buttons**:
   - Active filter button: Solid black capsule background (`--fg`) with white text (`--surface`).
   - Inactive buttons: Very light grey background (`--surface-hover`) with light border (`--border`) and dark text.
2. **Timeline Cards**:
   - Thin borders (`1px solid var(--border)`).
   - Highlighting state: Active/focused card gets a custom outline style: `2px dashed var(--highlight)` with a soft background tint, matching the annotation in the drawing.
3. **Information Rhythm**:
   - Title on the left, action controls (Language & Dark Mode) stick to the top right in rounded capsule borders.
   - Clean spacing with container width locked to `960px`.
