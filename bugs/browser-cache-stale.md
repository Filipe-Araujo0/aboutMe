2026-10-03T19:54:45-03:00

# Browser Reuses Stale Site Assets

The S3 objects were served without `Cache-Control` or `Expires`. Browsers can heuristically reuse such responses based on `Last-Modified`, so an ordinary reload may continue to display an older HTML document or asset. CloudFront invalidation only removes edge-cache entries; it cannot clear a visitor's browser cache. A hard reload bypasses the browser's cached copy, which explains why it displayed the new front.

Resolution (2026-10-04T07:57:15-03:00): set published objects to `Cache-Control: public, max-age=60, must-revalidate` and invalidate CloudFront after updating existing object metadata. This allows one minute of browser reuse, followed by mandatory revalidation.
