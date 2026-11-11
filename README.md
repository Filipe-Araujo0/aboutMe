# Filipe · Through time

Personal portfolio in English, with a timeline of independently styled versions and authored comparison pages.

The current chapter introduces Filipe as **Business Analyst & Developer** and adds selected open-source projects and upstream contributions. The project list covers AI-agent tooling, public data, developer analytics, API rate limits, and presentation files; the contribution list records two pull requests that were open on November 10, 2026. This addition was recorded on 2026-11-10T22:02:18-03:00.

## Build and run

Requires Node.js 18 or later and Python 3 (standard library only).

```sh
npm ci
npm run build
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Build output is static HTML, CSS, JavaScript and JSON in `dist/`; no backend is needed.

## Routes

- `/`: latest chapter (v4).
- `/versions/v1/index.html`: original React portfolio, rendered directly beside the timeline.
- `/versions/v2/index.html`: first editorial redesign.
- `/versions/v3/index.html`: professional introduction and working principles.
- `/versions/v4/index.html`: professional introduction, open-source projects, and contributions.
- `/changes/v1-v2/index.html`, `/changes/v2-v3/index.html`, and `/changes/v3-v4/index.html`: written comparisons.
- `/versions.json`: catalog consumed by the timeline.

Route inventory updated 2026-11-10T22:02:18-03:00.

Run the route check against the production host with `python3 scripts/check_version_routes.py --base-url https://filipeee0.com`.

The v1 date is based on content commit `1429ba5d5d526ad262e34832b37a9c2d8f6ba254`, dated November 2, 2025 in America/Sao_Paulo. It is a commit date, not the original launch date.

## Source organization

- `archive/v1/src/`: original React source.
- `build.py`: historical v1/v2 shells, content and styles.
- `build-archive.cjs`: original React bundle, using the automatic JSX runtime.
- `build-current.py`: v3, its comparison page and shared timeline catalog.
- `build-v4.py`: v4, its comparison page and latest catalog entry.
- `finalize_routes.py`: canonical `/index.html` URLs for nested static routes.

To add a chapter, preserve the earlier page and its assets, create a new version and comparison, update the catalog, and place the latest chapter at the root. Minor corrections to the current chapter can remain in that chapter.

## Existing AWS deployment

The existing Makefile and scripts are retained and still upload `dist/`. Neither this commit nor building the site publishes to AWS.

```sh
make deploy PURGE_ALL=true
```

Path behavior updated 2026-11-10T16:29:33-03:00: version and comparison links now use explicit `index.html` URLs because CloudFront's default root object does not resolve nested directories. The local Python server may serve slash-only directory URLs anyway, so verify the production host with the route-check script. Invalidate changed nested pages, styles, JavaScript and the version catalog as well as the root HTML; `PURGE_ALL=true` covers these.

Cache policy updated 2026-10-04T07:57:15-03:00: published objects use `Cache-Control: public, max-age=60, must-revalidate`, so browsers can reuse assets for one minute and revalidate afterward.

The independent Sites publication can be viewed at https://filipe-through-time.filipeee0.chatgpt.site.
