# Launch Checklist

1. Replace placeholder or missing source URLs in `data/sources.json` with DOI links, paper pages, official announcements, model cards, regulator pages, or authoritative reporting URLs.
2. Apply the data rules in [DATA-MODEL.md](../data/DATA-MODEL.md): every L2/L3 event needs enough independent sources, and every L3 event should include at least one primary source plus independent confirmation.
3. Every public Possible Direction must include at least two observed signals, and every signal must link to both published `eventIds` and supporting `sourceIds`.
4. Add `npm run validate:data` before deployment to check unique IDs, required fields, date formats, URL presence, score ranges, source counts, signal-to-event linkage, and `monitor_only` vs `consensus_gated` consistency.
5. Publish a concise public methodology page that explains inclusion criteria, source tiers, L1-L3 levels, Impact Score, consensus labels, Possible Direction signal rules, and why most directions remain `monitor_only`.
6. Bind the production domain, then add a real `sitemap.xml` and, if desired, `og:url` / canonical tags that point at that final domain.
7. If collecting votes, feedback, analytics, submissions, or contact messages, add privacy copy and store only the minimum needed data.
8. Follow [PRODUCT-PLAN.md](PRODUCT-PLAN.md): keep editorial content file-based for v1; use Cloudflare Pages for the site, Pages Functions + D1 for voting, and a separate Scheduled Worker only for candidate collection.
9. Run a final pass on Lighthouse, mobile screenshots, link validation, and source-link checks after deployment.
