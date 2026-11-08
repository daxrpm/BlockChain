SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

SCENES_DIR := src/ledger_viz/scenes
RENDERS_DIR := renders
# Uso: make preview SCENE=s00_smoke:Smoke
SCENE ?= s00_smoke:Smoke
SCENE_FILE = $(SCENES_DIR)/$(word 1,$(subst :, ,$(SCENE))).py
SCENE_CLASS = $(word 2,$(subst :, ,$(SCENE)))

.PHONY: help dev lint format typecheck test check preview render clips clips-preview clean

help: ## Lista los comandos disponibles
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'

dev: ## Instala dependencias (todas las groups)
	uv sync --all-groups

lint: ## Formato y lint sin modificar
	uv run ruff format --check
	uv run ruff check

format: ## Aplica formato y fixes automáticos
	uv run ruff format
	uv run ruff check --fix

typecheck: ## Chequeo de tipos con ty
	uv run ty check src tests

test: ## Tests del dominio con cobertura
	uv run pytest

check: lint typecheck test ## Todo lo anterior (antes de cada commit)

preview: ## Render rápido 480p de una escena: make preview SCENE=archivo:Clase
	uv run manim render -ql $(SCENE_FILE) $(SCENE_CLASS)

render: ## Render final 1080p30 + PNG del último fotograma a renders/
	uv run manim render -qh --fps 30 $(SCENE_FILE) $(SCENE_CLASS)
	uv run manim render -qh -s $(SCENE_FILE) $(SCENE_CLASS)
	mkdir -p $(RENDERS_DIR)
	find media/videos -path '*1080p30*' -name '$(SCENE_CLASS).mp4' -exec cp {} $(RENDERS_DIR)/ \;
	find media/images -name '$(SCENE_CLASS)*.png' -exec cp {} $(RENDERS_DIR)/$(SCENE_CLASS).png \;

clips-preview: ## Render rápido 480p de todos los clips de la parte 3 (para revisar)
	uv run manim render -ql --save_sections src/ledger_viz/scenes/part3.py Part3

clips: ## Clips finales 1080p30 (uno por diapositiva) + PNG de respaldo en renders/
	uv run manim render -qh --fps 30 --save_sections src/ledger_viz/scenes/part3.py Part3
	uv run python -m ledger_viz.export media/videos/part3/1080p30/sections/Part3.json $(RENDERS_DIR)

clean: ## Borra artefactos regenerables (media/ y cachés)
	rm -rf media .pytest_cache .ruff_cache .coverage
