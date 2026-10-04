# Filipe · Through time

Personal portfolio in English, with a timeline of independently styled versions and authored comparison pages.

The current chapter introduces Filipe as **Business Analyst & Developer**, covers business analysis, financial modeling and development with AI agents, and highlights curiosity and learning. It returns to the original light cards, rounded corners, soft shadows and blue-gray gradient. It does not name the employer or include a projects section.

## Build and run

Requires Node.js 18 or later and Python 3 (standard library only).

```sh
npm ci
npm run build
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Build output is static HTML, CSS, JavaScript and JSON in `dist/`; no backend is needed.

## Routes

- `/`: latest chapter (v3).
- `/versions/v1/`: original React portfolio, rendered directly beside the timeline.
- `/versions/v2/`: first editorial redesign.
- `/versions/v3/`: current professional introduction.
- `/changes/v1-v2/` and `/changes/v2-v3/`: written comparisons.
- `/versions.json`: catalog consumed by the timeline.

The v1 date is based on content commit `1429ba5d5d526ad262e34832b37a9c2d8f6ba254`, dated November 2, 2025 in America/Sao_Paulo. It is a commit date, not the original launch date.

## Source organization

- `archive/v1/src/`: original React source.
- `build.py`: historical v1/v2 shells, content and styles.
- `build-archive.cjs`: original React bundle, using the automatic JSX runtime.
- `build-current.py`: v3, its comparison page and shared timeline catalog.

To add a chapter, preserve the earlier page and its assets, create a new version and comparison, update the catalog, and place the latest chapter at the root. Minor corrections to the current chapter can remain in that chapter.

## Existing AWS deployment

The existing Makefile and scripts are retained and still upload `dist/`. Neither this commit nor building the site publishes to AWS.

```sh
make deploy PURGE_ALL=true
```

Historical pages require the host to resolve directory paths to their `index.html` files. CloudFront's default root object alone does not provide this for nested directories; configure a URI rewrite for directory requests, or use explicit `index.html` URLs. Invalidate changed nested pages, styles, JavaScript and the version catalog as well as the root HTML; `PURGE_ALL=true` covers these.

Cache policy updated 2026-10-04T07:57:15-03:00: published objects use `Cache-Control: public, max-age=60, must-revalidate`, so browsers can reuse assets for one minute and revalidate afterward.

The independent Sites publication can be viewed at https://filipe-through-time.filipeee0.chatgpt.site.
