# EpochArc Typography Preview · Design QA

## Comparison target

- Source visual truth: `reference/final-typography-target.png`
- Implementation URL: `http://127.0.0.1:4175/`
- Desktop implementation capture: `design-qa/implementation-desktop.png`
- Mobile implementation capture: `design-qa/implementation-mobile.png`
- Full-view comparison: `design-qa/comparison-desktop.png`
- Focused typography comparison: `design-qa/comparison-focus.png`
- State: Chinese, light theme, evidence ledger collapsed

## Viewport and normalization

- Source image: 1487 × 1058 px.
- Desktop implementation: 1440 × 1024 CSS px, 1440 × 1024 captured px, device density 1.
- Mobile test viewport: 390 × 844 CSS px; browser content capture 375 × 812 px after scrollbar/browser-surface reservation.
- The source and desktop implementation share a 1.405–1.406 aspect ratio. The full comparison normalizes both to 720 × 512 without cropping.
- The focused comparison crops the evidence-ledger region from each image and fits both regions into equal 720 × 480 frames.

## Required fidelity surfaces

### Fonts and typography

- Passed. The implementation uses the project system-font stack and the approved semantic roles rather than the generated image’s approximate pixels.
- Page title: `clamp(36px, 4.2vw, 48px) / 1.08 / 800`.
- Section title: `20px / 1.35 / 700`.
- Evidence title: `16px / 1.45 / 700`.
- Reading body: `15px / 1.7`.
- Supporting copy: `14px / 1.65`.
- Metadata and overlines: 12px and 11px.
- The implementation intentionally looks slightly more compact than the generated target because the written type specification is authoritative.

### Spacing and layout rhythm

- Passed. The stable single-column ledger, 24px row rhythm, hairline dividers, small numbered markers, source action alignment, and coral counter-condition block match the selected direction.
- The original mock's blue first-row rail was intentionally removed after review because the static first signal is not selected or current.
- The existing 220px EpochArc information rail remains outside the reading column. Its presence is an intentional product-shell constraint absent from the cropped visual target.
- Continuous prose is limited to 680px; evidence rows may use the full main-content width.

### Colors and visual tokens

- Passed. The implementation reuses the EpochArc light surface, foreground, muted gray, electric-blue accent, and coral counter-condition accent.
- Dark mode maps the same semantic roles to dark tokens and introduces no hard-coded light-only text colors.

### Image quality and asset fidelity

- Passed. The existing EpochArc SVG logo is reused as a real source asset.
- The selected Image Gen result is used only as visual reference; the production-like UI is rendered with semantic HTML and CSS.
- No raster placeholder, handcrafted icon, decorative illustration, or substituted logo is present.

### Copy and content

- Passed. The three evidence signals use the real Chinese and English direction copy.
- The implementation shows five sources for the third signal because the current direction content contains five public-source links; the generated target’s count of six is not treated as data truth.

## Interaction and responsive checks

- Source disclosure: passed. Each source-count button expands and collapses its associated source list and exposes `aria-expanded` / `aria-controls`.
- Language switch: passed for Chinese and English.
- Theme switch: passed for light and dark modes.
- Desktop overflow: none at 1440px.
- Mobile overflow: none at the 390px test viewport.
- Mobile reflow: signal rows become a two-column marker/content layout; the information rail moves below the article.
- Browser console: no warnings or errors.

## Comparison history

### Iteration 1

- [P2] Collapsed source lists remained visually rendered because `.source-list { display: grid; }` overrode the browser’s default `[hidden]` behavior.
- Fix: added `.source-list[hidden] { display: none; }`.
- Post-fix evidence: `design-qa/implementation-desktop.png` and `design-qa/comparison-focus.png`.
- Result: all three source lists are hidden in the collapsed state while their controlled DOM targets remain present.

### Remaining differences

- [P3] The generated target uses slightly larger apparent evidence titles and more open rows. The implementation keeps the approved 16px title and 24px row rhythm so it can become a reusable site token.
- [P3] The implementation includes the existing site header and external information rail. These are intentional shell elements, not typography drift.

## Final result

final result: passed
