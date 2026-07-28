# Prototype Instructions

Run the local server yourself and open the preview in the browser available to this environment. Do not give the user server-start instructions when you can run it.

Before making substantial visual changes, use the Product Design plugin's `get-context` skill when the visual source is unclear or no longer matches the current goal. When the user gives durable prototype-specific design feedback, preferences, or decisions, record them in `AGENTS.md`.

## Selected visual direction

- Use the stable single-column evidence ledger from visual option 1.
- Use option 3's hairline separators, condensed source action, and coral counter-condition treatment.
- Colored left rails must encode a real state: blue is reserved for an actual selected/current item, while red marks a counter-condition or risk. Static detail content does not receive a blue rail.
- Do not use the left contextual sidebar from option 2.
- The prototype must use the exact shared type roles documented in `docs/product/DESIGN-SYSTEM.md`; generated-image text sizing is inspirational, not authoritative.
- This is an isolated typography sample. Do not modify production templates until the user approves the rendered preview.

When implementing from a selected generated mock, treat that image as the source of truth for layout, component anatomy, density, spacing, color, typography, visible content, and hierarchy.

Build app UI in `src/`. Keep `.openai/hosting.json`, `worker/index.js`, `scripts/prepare-sites-build.mjs`, and `tests/sites-worker.test.mjs` intact so the same local prototype can be handed to Sites. Before a Sites handoff, run `npm run build` and `npm run test:sites`; the build must leave `dist/client/index.html`, `dist/server/index.js`, and `dist/.openai/hosting.json`.
