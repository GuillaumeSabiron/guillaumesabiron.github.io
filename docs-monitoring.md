# Audience and CV requests: private Cloudflare dashboard

## Metric contract

| Indicator | Source | Meaning / limits |
| --- | --- | --- |
| Visits / day | Cloudflare Web Analytics | Cloudflare's arrival/referrer-based metric; not unique people |
| Page views / day | Cloudflare Web Analytics | Observed HTML page views; extensions may block the beacon |
| CV requests FR / EN / day | Workers Analytics Engine | GET requests to the CV redirect, excluding HEAD and prefetch |
| Completed CV downloads | Not measured | A redirect does not prove that the PDF was received, opened or read |

Bots, repeat clicks and your own visits may still appear. Do not call the ratio
CV requests / visits a unique-person conversion rate. Direct PDF URLs bypass the
Worker. No visitor identifiers, IPs, referrers or user agents are added to the
Analytics Engine dataset by our code.

## 1. Visits and page views in Cloudflare

Open **Analytics → Web Analytics**, select `guillaumesabiron.github.io`, select
the last 30 days and the bot exclusion where available. Read Visits and Page
views by day. Use the same period and timezone when comparing charts.

The website beacon is already installed. Do not add a second one. A blocked
beacon means the request is absent from audience statistics; do not bypass a
visitor's blocker.

## 2. Daily CV requests in Cloudflare

Deploy `workers/cv-download-tracker/src/index.js` to the **existing** Worker
`guillaume-sabiron-cv-downloads`, keeping its existing `CV_DOWNLOADS` binding.
The website URL stays unchanged. Publishing the website does NOT publish the
Worker: it has its own deployment.

Open **Storage & databases → Analytics Engine**, click the dataset
`guillaume_sabiron_cv_downloads` to open **Studio**, and run
`workers/cv-download-tracker/daily-requests.sql`. This path and the query were
verified in this account on 5 November 2026. It returns UTC date,
language and weighted request count. Use a daily chart split by `cv_language`.
If the account UI does not expose SQL querying, use Cloudflare's SQL API or a
private Grafana dashboard; do not claim a dashboard exists merely because a
dataset was created.

The query filters `blob2 = 'cv_request'`, introduced by this Worker update.
Historical events without this field used a less strict counter and are not
silently mixed with the new series. No rows appear until the updated Worker
receives real requests. Preserve old data; do not manufacture test events in
production. Tests in this repo mock the dataset.

## 3. A single combined table

Web Analytics and Workers Analytics Engine are separate sources. Installing the
Worker does not automatically combine them. A unified table
`date | visits | page_views | cv_fr_requests | cv_en_requests` requires a private
dashboard joining Web Analytics GraphQL data and Analytics Engine SQL results.
It needs account access and scoped read credentials. Never put those credentials
or a public analytics endpoint in GitHub Pages. Until that private view is
configured, use the two native views with aligned UTC date ranges.

On 5 November 2026, the updated Worker version `4576591e` was activated in
Cloudflare. HEAD checks confirmed the correct FR/EN redirects and `no-store`
headers. The daily request query executed successfully in Studio with no new
events; no production test events were fabricated. The native Web Analytics
report showed no observed audience data over the selected last-30-days period.
That is not proof of zero human visitors (blocking and collection limits apply).

## Validation checklist

- Confirm the updated Worker deployment, not just the Pages deployment.
- Verify `/fr` and `/en` redirect to the matching CV with `Cache-Control: no-store`.
- HEAD health checks do not generate CV events.
- Confirm real visits reach Web Analytics; do not require ad blockers to be disabled.
- Compare only equal time windows. A missing day is not always proof of zero traffic.
- For long-term history, arrange private exports: do not assume indefinite retention.

Official references:
- https://developers.cloudflare.com/web-analytics/data-metrics/high-level-metrics/
- https://developers.cloudflare.com/analytics/analytics-engine/sql-api/
- https://developers.cloudflare.com/analytics/analytics-engine/sql-reference/date-time-functions/
