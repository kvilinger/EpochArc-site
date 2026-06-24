# Launch Checklist

1. Replace placeholder or missing source URLs in [data/events.json](/Users/gang/Documents/Project/WhereIsAIGoing/data/events.json) with DOI links, paper pages, official announcements, model cards, regulator pages, or authoritative reporting URLs.
2. Apply the v2 data rules in [DATA-MODEL.md](/Users/gang/Documents/Project/WhereIsAIGoing/DATA-MODEL.md): every L2/L3 event needs enough independent sources, and every L3 event should include at least one primary source plus independent confirmation.
3. Expand `data/forecasts.json` beyond provisional criteria: each public forecast needs source-backed supporting signals, counter-signals, achieved criteria, and not-achieved criteria.
4. Add `npm run validate:data` before deployment to check unique IDs, required fields, date formats, URL presence, score ranges, source counts, and forecast resolution criteria.
5. Publish a concise public methodology page that explains inclusion criteria, source tiers, L1-L3 levels, Impact Score, consensus labels, forecast resolution, corrections, and limitations.
6. Bind the production domain, then add a real `sitemap.xml` and, if desired, `og:url` / canonical tags that point at that final domain.
7. If collecting votes, feedback, analytics, submissions, or contact messages, add privacy copy and store only the minimum needed data.
8. Keep editorial content file-based for v1; use Cloudflare Pages for the site, Pages Functions + D1 for voting, and a separate Scheduled Worker only for candidate collection.
9. Run a final pass on Lighthouse, mobile screenshots, link validation, and source-link checks after deployment.
