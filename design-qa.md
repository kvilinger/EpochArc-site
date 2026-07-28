# EpochArc Production Typography Migration · Design QA

## Comparison target

- Source visual truth: `drafts/typography-system-preview/reference/final-typography-target.png`
- Written source of truth: `docs/product/DESIGN-SYSTEM.md`
- Direction implementation: `http://127.0.0.1:4174/directions/ai-software-teams/`
- Event implementation: `http://127.0.0.1:4174/events/kimi-k3-2026/`
- Arc implementation: `http://127.0.0.1:4174/arcs/ai-agents/`
- Direction desktop capture: `design-qa/production-direction-desktop.png`
- Direction mobile capture: `design-qa/production-direction-mobile.png`
- Event desktop capture: `design-qa/production-event-desktop.png`
- Arc desktop capture: `design-qa/production-arc-desktop.png`
- Full-view comparison: `design-qa/production-direction-comparison.png`
- State: Chinese, light theme, direction source disclosures collapsed.

## Viewport and normalization

- Source image: 1487 × 1058 px.
- Desktop test viewport: 1440 × 1100 CSS px; in-app browser content captures are 1425 × 1089 px at device density 1.
- Mobile test viewport: 390 × 844 CSS px; in-app browser content capture is 375 × 812 px after browser-surface reservation.
- Comparison image: both source and direction capture are fitted without cropping into equal 720 × 550 panels.
- Focused comparison: the source visual is itself the evidence-ledger region, and the production direction capture was taken with the evidence section aligned to the viewport. A separate crop was not needed.

## Required fidelity surfaces

### Fonts and typography

- Passed. All three production detail types use the documented semantic variables.
- Page title: `clamp(36px, 4.2vw, 44px) / 1.08 / 800`.
- Page lead: `17px / 1.65`.
- Section title: `20px / 1.35 / 700`.
- Item title: `16px / 1.45 / 700`.
- Reading body: `15px / 1.7`.
- Supporting copy: `14px / 1.65`.
- Metadata and overlines: 12px and 11px.
- Event section headings were promoted from `h3` to `h2`, so the visible hierarchy and document outline now agree.

### Spacing and layout rhythm

- Passed. Page headers, section gaps, item gaps, and module padding follow the shared 12/20/24/32/48px rhythm.
- Detail-page prose uses the full main-content measure instead of a nested 680px cap.
- Measured at 1440px: all three main columns and primary modules are 912px; arc module text is 862–878px after padding, and event/direction module text is 870px after padding.
- The overview rail is 220px with a 36px gap and remains outside the main column.
- Direction evidence uses the selected single-column ledger with hairline dividers, numbered markers, condensed source actions, and a coral counter-condition.
- Event detail retains the homepage timeline's evidence structure while using a neutral standalone-page surface and the shared type hierarchy.
- Arc detail retains continuous chapter reading, a restrained abstract module, and the same section/body roles; its chapter index now lives only in the shared right rail.
- At desktop width the 220px overview rail sits outside the 912–960px main content area. At narrower widths it follows the article.

### Colors and visual tokens

- Passed. All pages reuse `--fg`, `--muted`, `--border`, `--surface`, `--accent`, `--accent-soft`, and `--highlight`.
- Light and dark modes were checked on the direction page. No page-specific hard-coded text palette was introduced.

### Image quality and asset fidelity

- Passed. The existing EpochArc SVG logo remains the only visible brand image in the tested regions.
- No raster placeholder, emoji, CSS-drawn asset, or replacement logo was introduced.

### Copy and content

- Passed. English and Chinese event, arc, and direction content switched correctly.
- Direction source counts use the actual production data (2, 3, and 5 for the tested signals), not the approximate counts in the generated visual.

## Interaction and responsive checks

- Timeline return state: passed. Both browser Back and the event record back control return to the clean timeline URL with the originating node collapsed and positioned near its prior viewport location.
- Right-rail directory: passed on event, direction, and arc details. Scroll-spy updates the blue current item and `aria-current="location"`; optional missing sections remove their links.
- Source disclosure: passed. The source-count control expands a full-width two-column source list on desktop and a single-column list on mobile; it collapses again and exposes native `details` semantics.
- Language switch: passed on event, arc, and direction pages.
- Theme switch: passed in Chinese light and dark states.
- Desktop horizontal overflow: none at the 1440px test viewport.
- Mobile horizontal overflow: none at the 390px test viewport.
- Mobile rail order: passed; overview cards follow the main article.
- Right-rail directories: visible only while the rail is genuinely beside the content; hidden when the rail stacks below the article.
- The tested pages completed navigation, theme switching, language routing, and source expansion without a visible runtime failure.

## Comparison history

### Iteration 1

- [P2] Expanded direction source titles were constrained to the narrow action column and wrapped excessively.
- Fix: open source disclosures now span the content and action tracks; desktop sources use two columns and mobile sources use one.
- Post-fix evidence: `design-qa/production-direction-desktop.png`, browser interaction inspection, and `design-qa/production-direction-mobile.png`.

### Iteration 2

- [P2] Event content sections were visually upgraded but retained `h3` headings directly below the page `h1`.
- Fix: event summary, impact, consensus/sources, and related events now use `h2`.
- Post-fix evidence: `design-qa/production-event-desktop.png` and the browser-rendered heading outline.

### Iteration 3

- [P2] Blue left rails were reused on static direction, event, arc-summary, and insight content even though no item was selected.
- Fix: removed decorative blue rails and neutralized the standalone event surface. Blue rails are now reserved for real selected/current states; the red counter-condition rail remains because it has explicit caution semantics.
- Post-fix evidence: `design-qa/production-direction-desktop.png`, `design-qa/production-event-desktop.png`, and `design-qa/production-arc-desktop.png`.

### Iteration 4

- [P2] The arc abstract module incorrectly used the 680px reading measure as its outer width, so its border did not align with the chapter index and chapter content.
- Intermediate fix: the abstract module was expanded to the full 912px main column, but its paragraph incorrectly kept the legacy 680px cap.
- This intermediate state was rejected in Iteration 5 because it created a second content boundary.

### Iteration 5

- [P1] Keeping the old 680px prose cap inside the corrected 912px modules created a second, visibly narrower content boundary and excessive dead space.
- Fix: removed the nested prose cap from event, direction, and arc detail pages. Titles, summaries, narratives, insight text, assessments, questions, and evidence headers now consume the available main-content width; only explicit action columns reserve space.
- Post-fix evidence: updated desktop and mobile captures plus measured module/text widths for all three detail page types. At 1440px, arc/event/direction main columns each measured 912px with no horizontal overflow.

### Iteration 6

- [P1] Removing the old title cap allowed long detail-page titles to use the combined main-and-rail shell, so the event title visually entered the overview-rail region.
- Fix: at the wide-rail breakpoint, every `.page-with-rail` header now uses the exact width of the 912px main column. Below the breakpoint it remains fluid with the single-column layout.
- Post-fix evidence: arc, event, and direction headers each measured `[257, 1169, 912]`, exactly matching their main columns; the rail starts at 1205px. At the mobile test width, header and main content both measured 327px with zero horizontal overflow.

### Iteration 7

- [P1] The global balanced-wrap rule made long mixed Chinese/English titles break early even when usable content width remained, producing visibly truncated line lengths.
- Fix: detail-page titles now use natural/pretty wrapping inside the content column, and the shared maximum page-title size is 44px to prevent an orphaned final word at the 912px desktop measure.
- Post-fix evidence: the longest tested Chinese event title renders in two lines at both desktop widths. At 1440px the two line boxes measured 743px and 907px inside the 912px title/content column; at the reported 1050px viewport they measured 734px and 896px. Mobile remained overflow-free.

### Iteration 8

- [P1] Returning from a static event record reopened the timeline node because both the record back-link and the prior browser-history entry retained the event fragment.
- Fix: event record back-links now target the clean timeline URL, and internal “view on page” navigation replaces the expanded history entry before leaving the timeline. This applies to English and `/zh-hans/` routes.
- Post-fix evidence: after entering Kimi K3 from `#event=kimi-k3-2026`, browser Back returned to `/zh-hans/` with no details DOM; the in-page back control produced the same clean URL and collapsed item state.

### Iteration 9

- [P2] Detail pages had no unified way to show reading position; arc detail duplicated navigation in a sticky capsule row above the content.
- Fix: event, direction, and arc details now use a shared right-rail section directory with real anchors, scroll-spy updates, blue current-state styling, and `aria-current="location"`. The arc capsule row was removed.
- Post-fix evidence: bilingual production pages expose 4 event, 8 direction, and 7 arc directory entries; manual scrolling updated the active anchors for event evidence, direction counter-signal, and arc chapters. Missing optional event sections remove their directory links automatically.

### Iteration 10

- [P1] Returning from an event record correctly collapsed the originating timeline node but reset the page to the top, losing the reader's place.
- Fix: internal detail navigation records the originating event and its viewport anchor in the current history entry. Timeline restoration uses manual scroll history plus a short-lived return observer so it also works when Chromium restores the timeline from its back/forward cache; the temporary return fragment is removed after positioning.
- Post-fix evidence: Chinese browser Back restored Kimi K3 from item top 88px to 96px with the node collapsed; the Chinese record back control restored it to 120px. English browser Back restored the same node from 88px to 96px. All three returns ended at clean timeline URLs.

## Remaining differences

- [P3] The production direction page is denser than the generated target because it preserves the real site header, right overview rail, and exact documented type variables.
- [P3] The generated target omits baseline, consensus, questions, and source-registry sections. Production keeps them because they are real product content and now uses the same semantic hierarchy.

## Build note

- Event, direction, arc, Vite, and bilingual-page generation completed successfully.
- English and `/zh-hans/` production paths were checked from the built preview. Each returned the correct title, `lang`, canonical URL, and `en` / `zh-Hans` / `x-default` hreflang set.
- The isolated typography prototype build and its four Sites packaging tests passed.
- The aggregate validation command remains blocked by five errors in the concurrently edited `data/screening_log.json`. That file was not changed as part of this migration.

## Final result

final result: passed
