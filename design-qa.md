# EpochArc site-wide design system QA

## Comparison target

- Source visual truth:
  - `/Users/gang/.codex/generated_images/019f7d19-4d55-7e92-9f9a-ba53ae1b131f/exec-2f3f2657-360f-432c-9342-8889285434ea.png` (selected editorial structure)
  - `/Users/gang/.codex/generated_images/019f7d19-4d55-7e92-9f9a-ba53ae1b131f/exec-33fea254-ba46-4921-9fff-2884e86daaaf.png` (selected right-side information rail)
- Representative implementation: `http://127.0.0.1:4173/arcs/ai-agents/`
- Implementation screenshot: `/tmp/epocharc-design-qa-arc.png`
- Full-view comparison evidence: `/tmp/epocharc-design-qa-comparison.png`
- Focused header/navigation/summary/rail comparison: `/tmp/epocharc-design-qa-focused-comparison.png`
- Desktop viewport: 1440 × 1024, light theme, Chinese locale.
- Mobile viewport: 390 × 844, light theme, Chinese locale.

## Pages checked

- Arc detail: `/tmp/epocharc-design-qa-arc.png`
- Directions index: `/tmp/epocharc-design-qa-directions-list.png`
- Direction detail: `/tmp/epocharc-design-qa-direction-detail.png`
- Event detail: `/tmp/epocharc-design-qa-event-detail.png`
- Methodology: `/tmp/epocharc-design-qa-methods.png`
- Mobile arc: `/tmp/epocharc-design-qa-arc-mobile.png`
- Mobile direction detail: `/tmp/epocharc-design-qa-direction-detail-mobile.png`
- Mobile event after overflow and top-nav fixes: `/tmp/epocharc-design-qa-event-mobile-topnav-fixed.png`

## Findings

- No remaining P0, P1, or P2 mismatch was found.
- Fonts and typography: system sans and mono metadata remain consistent with the source direction; titles, body copy, and rail labels preserve a clear editorial hierarchy without clipping.
- Spacing and layout rhythm: every non-home page uses the 960px shell, left-aligned page header, unified return capsule, and the same 220px detail rail. List pages use the same outer grid without forcing a detail rail.
- Colors and visual tokens: existing near-white background, black text, cool gray borders, and electric-blue active state are reused in light and dark themes; no new gradients or heavy shadows were introduced.
- Image and asset fidelity: the existing EpochArc logo is retained. The design target does not require additional imagery, illustration, or generated assets.
- Copy and content: page-specific content remains intact. Methodology is explicitly presented as the single shared definition for footer and direction-review links.
- Icons: existing logo, language, theme, and return icon language is consistent across tested pages.
- Responsiveness: the information rail moves before long-form content below 820px, all tested 390px pages fit the viewport, and the chapter capsules remain horizontally scrollable.

## Comparison history

1. Initial mobile event-detail pass found a P2 horizontal overflow: long source URLs expanded the source list from 375px to 402px.
2. Fix: added `overflow-wrap: anywhere` and `word-break: break-word` to `.source-meta` in `src/css/detail.css`.
3. Post-fix evidence: the event detail reports `scrollWidth: 375` and `clientWidth: 375`; source metadata no longer overflows.
4. Initial mobile header pass showed cramped two-line navigation labels.
5. Fix: below 560px the wordmark text hides while the source logo remains, and navigation controls use compact, non-wrapping labels.
6. Post-fix evidence: `/tmp/epocharc-design-qa-event-mobile-topnav-fixed.png` shows the shared header fitting cleanly at 390 × 844.

## Functional checks

- Language selector switched the event page from Chinese to English and updated `document.documentElement.lang` to `en`.
- Theme control switched `body[data-theme]` from `light` to `dark` and was restored afterward.
- Arc chapter links, detail back links, event/source links, and methodology anchors remain semantic links.
- Active top-level navigation uses `aria-current="page"`.
- No browser console errors or warnings were present on the final tested state.
- Production build and content validation passed for 94 events, 272 sources, 4 directions, and 6 arcs. Existing data-quality warnings remain non-blocking and unrelated to this visual change.

## Follow-up polish

- P3: the direction index remains a ledger rather than adopting a sidebar; this is intentional because it is a collection page, not a single-record detail page.

final result: passed
