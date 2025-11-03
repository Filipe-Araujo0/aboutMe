SHELL := /bin/bash

.PHONY: help check build s3-sync invalidate deploy aws-cli-install

MAKEFLAGS += --no-builtin-rules

ENV_FILE := .env
ifneq (,$(wildcard $(ENV_FILE)))
include $(ENV_FILE)
export
endif

BUILD_DIR ?= dist
PURGE_ALL ?= false
EXTRA_PATHS ?=
WSL_DISTRIBUTION_ID ?=
WSL_BUCKET ?=
WSL_PROFILE ?=

DISTRIBUTION_ID ?= $(WSL_DISTRIBUTION_ID)
BUCKET ?= $(WSL_BUCKET)
PROFILE ?= $(WSL_PROFILE)

help:
	@echo "Targets disponíveis:"
	@echo "  make deploy              -> check + build + s3-sync + invalidate"
	@echo "  make build               -> npm run build"
	@echo "  make s3-sync             -> sincroniza $(BUILD_DIR) com s3://$${BUCKET}"
	@echo "  make invalidate          -> cria invalidacao no CloudFront"
	@echo "  make check               -> valida dependencias e credenciais AWS"
	@echo "  make aws-cli-install     -> instala/atualiza o aws-cli via scripts/install_aws_cli.sh"

check:
	@command -v aws >/dev/null 2>&1 || { echo "aws CLI não encontrado. Rode 'make aws-cli-install'."; exit 1; }
	@[ -n "$(PROFILE)" ] || { echo "Defina WSL_PROFILE (ou PROFILE) no ambiente ou .env."; exit 1; }
	@[ -n "$(BUCKET)" ] || { echo "Defina WSL_BUCKET (ou BUCKET) no ambiente ou .env."; exit 1; }
	@[ -n "$(DISTRIBUTION_ID)" ] || { echo "Defina WSL_DISTRIBUTION_ID (ou DISTRIBUTION_ID) no ambiente ou .env."; exit 1; }
	@aws sts get-caller-identity --profile "$(PROFILE)" >/dev/null

build:
	npm run build

s3-sync:
ifndef SKIP_CHECK
	@$(MAKE) --no-print-directory check
endif
	@[ -d "$(BUILD_DIR)" ] || { echo "Diretório de build inexistente: $(BUILD_DIR)"; exit 1; }
	@echo "Sincronizando $(BUILD_DIR) -> s3://$(BUCKET)"
	@aws s3 sync "$(BUILD_DIR)/" "s3://$(BUCKET)" --delete --only-show-errors --profile "$(PROFILE)"

invalidate:
ifndef SKIP_CHECK
	@$(MAKE) --no-print-directory check
endif
	@paths="/index.html"; \
	if [ "$(PURGE_ALL)" = "true" ]; then \
	  paths="/*"; \
	fi; \
	if [ -n "$(EXTRA_PATHS)" ]; then \
	  paths="$$paths $(EXTRA_PATHS)"; \
	fi; \
	echo "Invalidando CloudFront: $$paths"; \
	aws cloudfront create-invalidation --distribution-id "$(DISTRIBUTION_ID)" --paths $$paths --profile "$(PROFILE)"

deploy:
	@$(MAKE) --no-print-directory check
	@$(MAKE) --no-print-directory build
	@$(MAKE) --no-print-directory SKIP_CHECK=true s3-sync
	@$(MAKE) --no-print-directory SKIP_CHECK=true invalidate

aws-cli-install:
	./scripts/install_aws_cli.sh
