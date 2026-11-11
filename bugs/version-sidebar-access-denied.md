Written: 2026-11-10T16:22:36-03:00

# Version sidebar paths return AWS AccessDenied

## Observed behavior

The production homepage and `versions.json` load, but requests to all three
catalog version paths (`/versions/v1/`, `/versions/v2/`, `/versions/v3/`) and
both comparison paths return HTTP 403 with an AWS XML `AccessDenied` response.
The same paths return the expected pages from the local Python static server.
Requesting the corresponding production objects with an explicit
`/index.html` suffix returns HTTP 200 and the expected page titles.

The repeatable probe is `scripts/check_version_routes.py` (promoted from
temporary diagnostics on 2026-11-10T16:29:33-03:00). It checks the catalog
links, their comparison pages, HTTP status, response type, AWS denial body,
and version page title. Its local pass does not model the production origin's
path resolution.

## Causal chain

1. `build.py` and `build-current.py` write version and comparison pages as
   nested objects such as `dist/versions/v2/index.html` and
   `dist/changes/v1-v2/index.html`.
2. The generated `versions.json` stores directory URLs ending in `/`, and the
   comparison-page links in the build scripts use the same form. The timeline
   uses each catalog `path` as the version button destination.
3. Clicking a button therefore requests an object key such as
   `versions/v2/`, not `versions/v2/index.html`. The production host does not
   resolve nested directory URLs to their `index.html` objects. CloudFront's
   default root object handles the distribution root; it does not implicitly
   provide index-document behavior for each nested directory.
4. The requested directory key is absent. For S3 `GetObject`, an absent key
   can appear as HTTP 403 when the caller cannot list the bucket, which
   matches the observed AWS XML response. The explicit `index.html` object is
   readable, so this is a URL-to-object-key mismatch, not evidence that the
   page objects need broader read permissions.
5. The local `python3 -m http.server --directory dist` maps directory requests
   to `index.html`, so the same slash-terminated URLs pass locally and conceal
   the production-only failure. The latest page at `/` works because it is
   the distribution's root request.

## Fix direction

Generate explicit `/index.html` destinations for version and comparison
navigation. This uses objects already published to production and avoids
changing CloudFront or weakening S3 access controls. The production test must
pass against the actual domain after publishing the updated catalog and pages.

Resolution recorded 2026-11-10T16:29:33-03:00: `finalize_routes.py` now
canonicalizes the generated catalog and nested HTML links after the existing
build steps, and the route checker is retained as a reusable deployment test.

Production verification recorded 2026-11-10T17:45:30-03:00: uploaded only the
five version/comparison HTML objects and `versions.json` to `s3://filipeee0/`,
then completed CloudFront invalidation `I4FXUAMTI5E0SR8TIDFTK1F3WV`. The same
production route-check command now passes with HTTP 200 and the expected page
titles for all five routes. No objects were deleted and no access policies
were changed.

## References

- [CloudFront default root object behavior](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DefaultRootObject.html)
- [Amazon S3 GetObject: missing-object response and permissions](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html)
