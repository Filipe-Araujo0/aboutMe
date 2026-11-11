"""Build portfolio version 4 and its comparison with version 3."""

from __future__ import annotations

import json
import re
from pathlib import Path

BUILD_DIR = Path("dist")
VERSION_TITLE = "Open-source projects & contributions"
VERSION_DESCRIPTION = (
    "Selected open-source projects and upstream contributions by Filipe."
)
HERO_ACTIONS = """<div class="open-source__actions"><a href="#open-source">Explore open-source work <span aria-hidden="true">↓</span></a><a href="https://github.com/Filipe-Araujo0">GitHub profile <span aria-hidden="true">↗</span></a></div>"""

OPEN_SOURCE_SECTION = """<section class="card open-source" id="open-source">
<div class="open-source__header"><div><p class="open-source__eyebrow">Open source / selected work</p><h2>Projects I build &amp; share.</h2></div><p>Small tools for practical problems, published with their source code.</p></div>
<ul class="open-source__projects">
<li class="open-source__project"><p class="open-source__meta">AI agent tooling · Python</p><h3><a href="https://github.com/Filipe-Araujo0/tell-me-jev">tmjev <span aria-hidden="true">↗</span></a></h3><p>Turns noisy test, build, and tool output into compact, typed next-step JSON for AI coding agents.</p></li>
<li class="open-source__project"><p class="open-source__meta">Public data · Python</p><h3><a href="https://github.com/Filipe-Araujo0/pydatajud">pydatajud <span aria-hidden="true">↗</span></a></h3><p>A Python client for the CNJ’s public DataJud API, including batch checks for new case movements.</p></li>
<li class="open-source__project"><p class="open-source__meta">Developer analytics · Python</p><h3><a href="https://github.com/Filipe-Araujo0/opencode-stats">OpenCode Stats <span aria-hidden="true">↗</span></a></h3><p>Local, read-only reports from the usage data persisted by OpenCode.</p></li>
<li class="open-source__project"><p class="open-source__meta">API infrastructure · Python</p><h3><a href="https://github.com/Filipe-Araujo0/access_api">Access API Proxy <span aria-hidden="true">↗</span></a></h3><p>Shares upstream API rate limits across callers and retries temporary rate-limit and availability errors.</p></li>
<li class="open-source__project"><p class="open-source__meta">Presentations · Python</p><h3><a href="https://github.com/Filipe-Araujo0/translate_pptx">translate_pptx <span aria-hidden="true">↗</span></a></h3><p>Translates or rewrites slide text while preserving layout, formatting, and the rest of the deck.</p></li>
</ul>
<div class="open-source__contributions"><div class="open-source__contribution-heading"><div><p class="open-source__eyebrow">Upstream contributions</p><h3>Work beyond my own repositories.</h3></div><p>Two public pull requests were open when this chapter was published.</p></div>
<ul class="contribution-list">
<li><div class="contribution-list__meta"><span>Ory · Lumen · PR #199</span><span class="contribution-list__status">Open</span></div><a href="https://github.com/ory/lumen/pull/199">Make the Lumen OpenCode plugin compatible with V2 <span aria-hidden="true">↗</span></a></li>
<li><div class="contribution-list__meta"><span>Gemini Research MCP · PR #22</span><span class="contribution-list__status">Open</span></div><a href="https://github.com/machinemates-ai/gemini-research-mcp/pull/22">Make web research interactions continuable <span aria-hidden="true">↗</span></a></li>
</ul>
<p class="open-source__snapshot">Pull-request status in this snapshot: November 10, 2026.</p>
<a class="open-source__profile" href="https://github.com/Filipe-Araujo0">Browse all my public work on GitHub <span aria-hidden="true">↗</span></a></div>
</section>"""

COMPARISON_CONTENT = """<header class="hero"><h1 class="hero__title">What changed</h1><p class="hero__eyebrow">Version 03 → Version 04</p><p class="hero__metadata">November 10, 2026</p><p class="hero__summary">The professional introduction remains; this chapter adds concrete examples of open-source work and contributions to other projects.</p><div class="version-actions"><a href="/versions/v3/index.html">View version 03</a><a href="/versions/v4/index.html">View version 04</a></div></header>
<section class="card card-entry"><h2>From principles to examples</h2><p>Version 03 described my work in business analysis, financial modeling, internal systems, and software development. Version 04 keeps that context and adds a dedicated area where visitors can explore projects I publish and maintain.</p></section>
<section class="card"><h2>Selected open-source projects</h2><p>Five repositories show different practical problems I work on: AI-agent tooling, public data, developer analytics, API rate limits, and presentation files. Each project name links directly to its source.</p><p><a href="/versions/v4/index.html#open-source">Explore the project list in version 04</a></p></section>
<section class="card"><h2>Contributions to other projects</h2><p>The new area also records two upstream pull requests that were open on November 10, 2026: one for the Ory Lumen OpenCode plugin and another for Gemini Research MCP.</p><p>The earlier versions remain available in the history timeline.</p></section>"""

V4_STYLES = """
.open-source__actions{display:flex;flex-wrap:wrap;gap:1.25rem;margin-top:1.35rem;font-size:.95rem}.open-source__actions a,.open-source__project h3 a,.contribution-list a,.open-source__profile{transition:color .2s ease,transform .2s ease;text-decoration:none}.open-source__actions a:hover,.open-source__actions a:focus-visible,.open-source__project h3 a:hover,.open-source__project h3 a:focus-visible,.contribution-list a:hover,.contribution-list a:focus-visible,.open-source__profile:hover,.open-source__profile:focus-visible{color:#2563eb}.open-source__header,.open-source__contribution-heading{display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:end}.open-source__header{margin-bottom:1.5rem}.open-source__header h2,.open-source__contribution-heading h3{margin:.2rem 0 0}.open-source__header>p,.open-source__contribution-heading>p{margin:0;color:#64748b;line-height:1.7}.open-source__eyebrow,.open-source__meta{margin:0;color:#64748b;font-size:.78rem;letter-spacing:.04em}.open-source__projects,.contribution-list{list-style:none;margin:0;padding:0}.open-source__projects{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:2rem}.open-source__project{border-top:1px solid #e2e8f0;padding:1rem 0 1.15rem}.open-source__project h3{font-size:1.08rem;margin:.35rem 0}.open-source__project h3 a{display:inline-flex;gap:.45rem;align-items:center}.open-source__project h3 a span,.contribution-list a span,.open-source__profile span{color:#64748b}.open-source__project>p:last-child{margin:0;color:#475569;line-height:1.65}.open-source__contributions{border-top:1px solid #cbd5e1;margin-top:1.5rem;padding-top:1.5rem}.open-source__contribution-heading{margin-bottom:1rem}.contribution-list li{border-top:1px solid #e2e8f0;padding:.85rem 0}.contribution-list__meta{display:flex;justify-content:space-between;gap:1rem;color:#64748b;font-size:.8rem;margin-bottom:.25rem}.contribution-list__status{white-space:nowrap}.contribution-list a{line-height:1.6}.open-source__snapshot{font-size:.78rem;color:#64748b;margin:.5rem 0 1rem}.open-source__profile{font-weight:600}.open-source__actions a:hover,.open-source__project h3 a:hover,.contribution-list a:hover,.open-source__profile:hover{transform:translateX(2px)}@supports (animation-timeline:view()){.open-source__project{animation:project-reveal linear both;animation-timeline:view();animation-range:entry 0% entry 45%}}@keyframes project-reveal{from{opacity:.55;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}@media(max-width:760px){.open-source__header,.open-source__contribution-heading,.open-source__projects{grid-template-columns:1fr}.open-source__header,.open-source__contribution-heading{gap:.75rem}.open-source__projects{column-gap:0}}@media(prefers-reduced-motion:reduce){.open-source__actions a,.open-source__project h3 a,.contribution-list a,.open-source__profile{transition:none}.open-source__project{animation:none!important}}
"""


def replace_once(text: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(
        pattern, lambda _: replacement, text, count=1, flags=re.DOTALL
    )
    assert count == 1, f"Expected one match for generated-page pattern: {pattern}"
    return updated


def set_page_metadata(page: str, title: str, description: str) -> str:
    page = replace_once(page, r"<title>.*?</title>", f"<title>{title} · Filipe</title>")
    return replace_once(
        page,
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{description}">',
    )


def replace_main(page: str, content: str) -> str:
    opening_tag = '<main class="page">'
    start = page.index(opening_tag) + len(opening_tag)
    end = page.index("</main>", start)
    assert start < end, "The version template must contain one main page region"
    return f"{page[:start]}{content}{page[end:]}"


def main() -> None:
    source_path = BUILD_DIR / "versions/v3/index.html"
    assert source_path.is_file(), "Build version 3 before generating version 4"
    version3_page = source_path.read_text(encoding="utf-8")

    version4_page = replace_once(
        version3_page,
        r'<p class="hero__summary">.*?</p>',
        '<p class="hero__summary">I build tools for analysis, APIs, documents, and AI workflows—and share selected projects and upstream contributions in open source.</p>',
    )
    metadata_marker = '<p class="hero__metadata">'
    assert version4_page.count(metadata_marker) == 1, (
        "Version 3 must have one hero metadata line for version 4"
    )
    version4_page = version4_page.replace(
        metadata_marker, f"{HERO_ACTIONS}{metadata_marker}", 1
    )
    version4_page = replace_once(
        version4_page,
        r'<p class="hero__metadata">.*?</p>',
        '<p class="hero__metadata">São Paulo, Brazil · Updated November 10, 2026</p>',
    )
    footer_marker = '<footer class="card" id="contact">'
    assert version4_page.count(footer_marker) == 1, (
        "Version 3 must have one contact footer for the open-source section"
    )
    version4_page = version4_page.replace(
        footer_marker, f"{OPEN_SOURCE_SECTION}\n{footer_marker}", 1
    )
    version4_page = set_page_metadata(version4_page, VERSION_TITLE, VERSION_DESCRIPTION)

    css_path = BUILD_DIR / "current.css"
    css_path.write_text(
        css_path.read_text(encoding="utf-8") + V4_STYLES, encoding="utf-8"
    )

    version4_path = BUILD_DIR / "versions/v4/index.html"
    version4_path.parent.mkdir(parents=True, exist_ok=True)
    version4_path.write_text(version4_page, encoding="utf-8")
    (BUILD_DIR / "index.html").write_text(version4_page, encoding="utf-8")

    comparison = replace_main(version3_page, COMPARISON_CONTENT)
    comparison = set_page_metadata(
        comparison,
        "Changes · V03 to V04",
        "What changed in Filipe’s portfolio between versions 03 and 04.",
    )
    comparison_path = BUILD_DIR / "changes/v3-v4/index.html"
    comparison_path.parent.mkdir(parents=True, exist_ok=True)
    comparison_path.write_text(comparison, encoding="utf-8")

    catalog_path = BUILD_DIR / "versions.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    assert catalog["latest"] == "v3", "Build version 4 after the version 3 generator"
    assert all(item["id"] != "v4" for item in catalog["versions"]), (
        "The generated version catalog must not already contain version 4"
    )
    version3 = next(item for item in catalog["versions"] if item["id"] == "v3")
    version3["pageTitle"] = "Business Analyst & Developer"
    catalog["latest"] = "v4"
    catalog["versions"].insert(
        0,
        {
            "id": "v4",
            "date": "2026-11-10",
            "title": VERSION_TITLE,
            "path": "/versions/v4/",
            "changes": "/changes/v3-v4/",
        },
    )
    catalog_path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
