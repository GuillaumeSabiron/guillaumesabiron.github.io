# CV download tracker

This Worker records one anonymous event for each requested CV variant, then
returns a `302` redirect to the PDF served by GitHub Pages.

Only the variant (`fr` or `en`), event type (`cv_request`) and event timestamp are written to Workers
Analytics Engine. It does not store IP addresses, user agents, referrers, or
other visitor identifiers.

## Deploy

1. In the Cloudflare dashboard, open **Workers & Pages** and the existing Worker.
2. Its name is `guillaume-sabiron-cv-downloads`; do not create a duplicate.
3. In **Settings → Bindings**, add an **Analytics Engine** binding named
   `CV_DOWNLOADS` with the dataset `guillaume_sabiron_cv_downloads`.
4. Replace the Worker code with `src/index.js` and deploy it.
5. Copy the resulting `*.workers.dev` URL. The public CV links will then use:
   - `https://YOUR-WORKER.workers.dev/fr`
   - `https://YOUR-WORKER.workers.dev/en`

The existing URL is already linked from the website. HEAD requests, unsupported
methods and browser prefetches are not counted. Repeat GETs and bots can still
count; this is not a unique-person or completed-download metric. A measurement
failure does not block the redirect. Responses use `Cache-Control: no-store`.

Run `npm run test:worker` at the repository root. See `daily-requests.sql` and
the root `docs-monitoring.md` for the daily Cloudflare query and metric definitions.
