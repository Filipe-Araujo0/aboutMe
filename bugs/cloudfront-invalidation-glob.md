2026-10-03T15:45:58-03:00

# CloudFront Invalidation Path Expansion

When `PURGE_ALL=true`, the Makefile assigns `/*` to `paths` and expands `$paths` unquoted in the shell command for `aws cloudfront create-invalidation`. Because pathname expansion is enabled, Bash replaces `/*` with entries from the local filesystem root. CloudFront then accepts those unrelated paths, leaving the site's cached objects not invalidated. The deploy inputs are valid; the failure occurs at the shell-to-AWS CLI argument boundary. Disable pathname expansion for that recipe while retaining word splitting for multiple `EXTRA_PATHS` entries.
