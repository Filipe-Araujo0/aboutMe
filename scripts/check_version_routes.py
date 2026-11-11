"""Check that every version link in the published catalog opens its page."""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


class PageTitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.parts.append(data)


class SiteNavigationParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        target = (
            attributes.get("href")
            if tag == "a"
            else attributes.get("src")
            if tag == "iframe"
            else None
        )
        if not target:
            return
        path = urlsplit(target).path
        if path.startswith(("/versions/", "/changes/", "/archive/")):
            self.targets.append(path)


def fetch(url: str) -> tuple[int, str, str, str]:
    request = Request(url, headers={"User-Agent": "aboutme-version-route-check/1.0"})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=15) as response:
                body = response.read(64 * 1024).decode("utf-8", errors="replace")
                return (
                    response.status,
                    response.geturl(),
                    response.headers.get("Content-Type", ""),
                    body,
                )
        except HTTPError as error:
            body = error.read(64 * 1024).decode("utf-8", errors="replace")
            return (
                error.code,
                error.geturl(),
                error.headers.get("Content-Type", ""),
                body,
            )
        except URLError as error:
            if attempt == 2:
                return 0, url, "", str(error.reason)
            sleep(0.5)
    raise AssertionError(
        "A route request must either return or exhaust its bounded retries"
    )


def page_title(body: str) -> str:
    parser = PageTitleParser()
    parser.feed(body)
    return " ".join("".join(parser.parts).split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url", required=True, help="Site origin, e.g. https://example.com"
    )
    parser.add_argument(
        "--force-index-html",
        action="store_true",
        help="Probe directory links as explicit index.html objects to verify the host workaround",
    )
    args = parser.parse_args()
    parts = urlsplit(args.base_url)
    if (
        parts.scheme not in {"http", "https"}
        or not parts.netloc
        or parts.path not in {"", "/"}
    ):
        parser.error("--base-url must be an HTTP(S) origin without a path")
    base_url = f"{parts.scheme}://{parts.netloc}/"
    failures: list[str] = []

    root_status, root_url, root_type, root_body = fetch(base_url)
    if root_status != 200 or "text/html" not in root_type.lower():
        failures.append(
            f"homepage returned HTTP {root_status} ({root_type}) at {root_url}"
        )
    if "accessdenied" in root_body.lower():
        failures.append("homepage contains an AWS AccessDenied response")

    catalog_url = urljoin(base_url, "versions.json")
    catalog_status, catalog_final_url, catalog_type, catalog_body = fetch(catalog_url)
    if catalog_status != 200 or "json" not in catalog_type.lower():
        failures.append(
            f"version catalog returned HTTP {catalog_status} ({catalog_type}) at {catalog_final_url}"
        )
        versions: list[dict[str, str]] = []
        latest = ""
    else:
        try:
            catalog = json.loads(catalog_body)
            if not isinstance(catalog, dict):
                raise TypeError("catalog must be an object")
            versions = catalog["versions"]
            latest = catalog["latest"]
            if not isinstance(versions, list) or not isinstance(latest, str):
                raise TypeError("catalog has invalid versions or latest fields")
            if any(not isinstance(version, dict) for version in versions):
                raise TypeError("catalog version entries must be objects")
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            failures.append(f"version catalog is invalid: {type(error).__name__}")
            versions = []
            latest = ""

    if not versions:
        failures.append("version catalog contains no version links")

    pending: list[tuple[str, str, str]] = []
    for version in versions:
        version_id = version.get("id", "")
        path = version.get("path", "")
        match = re.fullmatch(r"/versions/(v\d+)/(?:index\.html)?", path)
        if not match or match.group(1) != version_id:
            failures.append(
                f"{version_id or '<unknown>'}: invalid catalog path {path!r}"
            )
            continue
        expected_title = (
            f"Version {int(version_id[1:]):02d}"
            if version_id != latest
            else version.get("title", "")
        )
        pending.append((path, expected_title, version_id))
        changes = version.get("changes", "")
        if changes:
            if re.fullmatch(r"/changes/v\d+-v\d+/(?:index\.html)?", changes):
                pending.append((changes, "", f"{version_id} comparison"))
            else:
                failures.append(f"{version_id}: invalid comparison path {changes!r}")

    checked = 0
    seen: set[str] = set()
    while pending:
        path, expected_title, label = pending.pop(0)
        if path in seen:
            continue
        seen.add(path)
        request_path = path
        if args.force_index_html and not request_path.endswith("/index.html"):
            request_path = f"{request_path.rstrip('/')}/index.html"
        target_url = urljoin(base_url, request_path.lstrip("/"))
        status, final_url, content_type, body = fetch(target_url)
        title = page_title(body)
        checked += 1
        print(f"HTTP {status} {path} -> {final_url} | {title or content_type}")

        if status != 200:
            failures.append(f"{label}: route returned HTTP {status}")
        if "text/html" not in content_type.lower():
            failures.append(
                f"{label}: expected HTML but received {content_type or 'no Content-Type'}"
            )
        if "accessdenied" in body.lower():
            failures.append(f"{label}: response contains AWS AccessDenied")
        if expected_title and expected_title.casefold() not in title.casefold():
            failures.append(
                f"{label}: expected page title containing {expected_title!r}, got {title!r}"
            )

        if status == 200 and "text/html" in content_type.lower():
            links = SiteNavigationParser()
            links.feed(body)
            pending.extend(
                (nested_path, "", "nested navigation") for nested_path in links.targets
            )

    print(f"Checked {checked} version and nested navigation routes from {base_url}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("PASS: version sidebar, comparison, and nested routes resolve to their pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
