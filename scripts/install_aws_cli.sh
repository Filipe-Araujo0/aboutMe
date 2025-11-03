#!/usr/bin/env bash
set -euo pipefail

# Instalando ou atualizando o aws-cli de forma idempotente.
if ! command -v aws >/dev/null 2>&1; then
  sudo apt-get update -y
  sudo apt-get install -y unzip curl
fi

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -o awscliv2.zip
sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update
rm -f awscliv2.zip
rm -rf aws

# Ativando o auto-complete
grep -qxF "complete -C '/usr/local/bin/aws_completer' aws" ~/.bashrc || echo "complete -C '/usr/local/bin/aws_completer' aws" >> ~/.bashrc
source ~/.bashrc
