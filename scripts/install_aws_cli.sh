#!/usr/bin/env bash
set -euo pipefail

command -v curl >/dev/null 2>&1 || { echo "curl nao encontrado; instale-o pelo gerenciador disponivel no sistema" >&2; exit 1; }
command -v unzip >/dev/null 2>&1 || { echo "unzip nao encontrado; instale-o pelo gerenciador disponivel no sistema" >&2; exit 1; }

case "$(uname -m)" in
  x86_64) AWS_ARCH="x86_64" ;;
  aarch64|arm64) AWS_ARCH="aarch64" ;;
  *) echo "Arquitetura nao suportada: $(uname -m)" >&2; exit 1 ;;
esac

INSTALL_DIR="${HOME}/.local/aws-cli"
BIN_DIR="${HOME}/.local/bin"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

mkdir -p "$BIN_DIR"
curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-${AWS_ARCH}.zip" -o "${TEMP_DIR}/awscliv2.zip"
unzip -q "${TEMP_DIR}/awscliv2.zip" -d "$TEMP_DIR"
"${TEMP_DIR}/aws/install" --bin-dir "$BIN_DIR" --install-dir "$INSTALL_DIR" --update

echo "AWS CLI instalado em ${BIN_DIR}/aws"
case ":${PATH}:" in
  *":${BIN_DIR}:"*) ;;
  *) echo "Adicione ${BIN_DIR} ao PATH para usar aws e make deploy." ;;
esac
