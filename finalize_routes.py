"""Finalize static routes for hosts without nested-directory index resolution."""

import json
import re
from pathlib import Path

BUILD_DIR = Path("dist")
ROUTE_BASE = r"/(?:versions/v\d+|changes/v\d+-v\d+|archive/v\d+)"
CATALOG_ROUTE = re.compile(f"{ROUTE_BASE}$")
HTML_ROUTE = re.compile(rf"(?P<route>{ROUTE_BASE})/(?=[\"'?#\s]|$)")


def explicit_index_path(path: str) -> str:
    if path.endswith("/") and CATALOG_ROUTE.fullmatch(path[:-1]):
        return f"{path}index.html"
    return path


def main() -> None:
    catalog_path = BUILD_DIR / "versions.json"
    assert catalog_path.is_file(), (
        "Build must produce versions.json before route finalization"
    )
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    assert isinstance(catalog, dict), "Generated version catalog must be a JSON object"
    assert isinstance(catalog["versions"], list), (
        "Generated version catalog must contain a versions list"
    )

    for version in catalog["versions"]:
        version["path"] = explicit_index_path(version["path"])
        if "changes" in version:
            version["changes"] = explicit_index_path(version["changes"])

    catalog_path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")

    for html_path in BUILD_DIR.rglob("*.html"):
        original = html_path.read_text(encoding="utf-8")
        finalized = HTML_ROUTE.sub(r"\g<route>/index.html", original)
        if finalized != original:
            html_path.write_text(finalized, encoding="utf-8")


if __name__ == "__main__":
    main()
