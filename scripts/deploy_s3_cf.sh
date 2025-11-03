#!/usr/bin/env bash
set -euo pipefail

# Deploy estatico para S3 + invalidacao CloudFront.
# Decisao: invalidar somente HTML por padrao para baratear cache-busting; permitir PURGE_ALL quando estritamente necessario.

DISTRIBUTION_ID="${WSL_DISTRIBUTION_ID:-${DISTRIBUTION_ID:-}}"
BUCKET="${WSL_BUCKET:-${BUCKET:-}}"
PROFILE="${WSL_PROFILE:-${PROFILE:-}}"

: "${DISTRIBUTION_ID:?Defina WSL_DISTRIBUTION_ID ou DISTRIBUTION_ID no ambiente}"
: "${BUCKET:?Defina WSL_BUCKET ou BUCKET no ambiente}"
: "${PROFILE:?Defina WSL_PROFILE ou PROFILE no ambiente}"

BUILD_DIR="${BUILD_DIR:-./dist}"
PURGE_ALL="${PURGE_ALL:-false}"
EXTRA_PATHS="${EXTRA_PATHS:-}"

command -v aws >/dev/null 2>&1 || { echo "aws CLI nao encontrado"; exit 1; }

if [ -f package.json ] && command -v npm >/dev/null 2>&1; then
  echo "Detectado package.json; executando npm run build"
  npm run build
fi

[ -d "$BUILD_DIR" ] || { echo "Diretorio de build inexistente: $BUILD_DIR"; exit 1; }

echo "Subindo para s3://$BUCKET a partir de $BUILD_DIR"
aws s3 sync "$BUILD_DIR/" "s3://$BUCKET" --delete --only-show-errors --profile "$PROFILE"

PATHS="/index.html"
if [ "$PURGE_ALL" = "true" ]; then
  PATHS="/*"
fi
if [ -n "$EXTRA_PATHS" ]; then
  PATHS="$PATHS $EXTRA_PATHS"
fi

echo "Invalidando CloudFront: $PATHS"
aws cloudfront create-invalidation --distribution-id "$DISTRIBUTION_ID" --paths $PATHS --profile "$PROFILE"

echo "OK: Deploy + invalidacao concluido"
