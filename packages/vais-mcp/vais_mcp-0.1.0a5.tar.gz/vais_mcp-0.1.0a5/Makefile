# Optional variables with default values.
IMPERSONATE_SERVICE_ACCOUNT ?=
VAIS_LOCATION ?= global
PAGE_SIZE ?= 5
MAX_EXTRACTIVE_SEGMENT_COUNT ?= 2
MCP_PORT ?= 8000
MCP_HOST ?= 0.0.0.0
LOG_LEVEL ?= WARNING
# For any additional arguments to pass to the uvicorn command (via 'uv run vais-mcp').
# Example: make run ARGS="--reload"
ARGS ?=

.PHONY: run
run:
	@if [ -z "$(GOOGLE_CLOUD_PROJECT_ID)" ]; then \
		echo "Error: GOOGLE_CLOUD_PROJECT_ID is not set. Please set it as an environment variable or pass it as an argument."; \
		exit 1; \
	fi
	@if [ -z "$(VAIS_ENGINE_ID)" ]; then \
		echo "Error: VAIS_ENGINE_ID is not set. Please set it as an environment variable or pass it as an argument."; \
		exit 1; \
	fi
	@echo "--- Starting Vertex AI Search MCP (local) ---"
	@echo "Configuration (from environment/Makefile defaults):"
	@echo "  GOOGLE_CLOUD_PROJECT_ID        : $(GOOGLE_CLOUD_PROJECT_ID)"
	@echo "  IMPERSONATE_SERVICE_ACCOUNT    : $(IMPERSONATE_SERVICE_ACCOUNT)"
	@echo "  VAIS_ENGINE_ID                 : $(VAIS_ENGINE_ID)"
	@echo "  VAIS_LOCATION                  : $(VAIS_LOCATION)"
	@echo "  PAGE_SIZE                      : $(PAGE_SIZE)"
	@echo "  MAX_EXTRACTIVE_SEGMENT_COUNT   : $(MAX_EXTRACTIVE_SEGMENT_COUNT)"
	@echo "  MCP_HOST                       : $(MCP_HOST)"
	@echo "  MCP_PORT                       : $(MCP_PORT)"
	@echo "  LOG_LEVEL                      : $(LOG_LEVEL)"
	@echo "  Additional ARGS to uv run      : $(ARGS)"
	@echo "---"
	PYTHONPATH=src \
	GOOGLE_CLOUD_PROJECT_ID="$(GOOGLE_CLOUD_PROJECT_ID)" \
	IMPERSONATE_SERVICE_ACCOUNT="$(IMPERSONATE_SERVICE_ACCOUNT)" \
	VAIS_ENGINE_ID="$(VAIS_ENGINE_ID)" \
	VAIS_LOCATION="$(VAIS_LOCATION)" \
	PAGE_SIZE=$(PAGE_SIZE) \
	MAX_EXTRACTIVE_SEGMENT_COUNT=$(MAX_EXTRACTIVE_SEGMENT_COUNT) \
	MCP_HOST="$(MCP_HOST)" \
	MCP_PORT="$(MCP_PORT)" \
	LOG_LEVEL="$(LOG_LEVEL)" \
	uv run vais-mcp $(ARGS)

# Example usage:
#   make run GOOGLE_CLOUD_PROJECT_ID=my-project VAIS_ENGINE_ID=my-engine
#   export GOOGLE_CLOUD_PROJECT_ID=my-project; export VAIS_ENGINE_ID=my-engine; make run
#   make run GOOGLE_CLOUD_PROJECT_ID=my-project VAIS_ENGINE_ID=my-engine ARGS="--reload" (Uvicorn's --reload flag)

.PHONY: test
test:
	uv run pytest

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  run       - Run the Vertex AI Search MCP application with current configuration."
	@echo "              Mandatory: GOOGLE_CLOUD_PROJECT_ID, VAIS_ENGINE_ID (set via env or make arg)."
	@echo "              Override optional variables: make run VAR=value"
	@echo "              Pass additional uvicorn args: make run ARGS=\\"--reload\\""
	@echo "  help      - Show this help message."

# Set 'help' as the default target
.DEFAULT_GOAL := help 