#!/bin/bash
# Hobbyist AI - Quick Start Scripts
# Run these from the backend directory

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== Hobbyist AI Backend ===${NC}"

case "${1:-dev}" in
    dev)
        echo -e "${GREEN}Starting development server...${NC}"
        uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ;;
    
    tests)
        echo -e "${GREEN}Running tests...${NC}"
        uv run pytest -v
        ;;
    
    lint)
        echo -e "${GREEN}Running linting...${NC}"
        uv run ruff check .
        ;;
    
    format)
        echo -e "${GREEN}Formatting code...${NC}"
        uv run black .
        uv run ruff check . --fix
        ;;
    
    sync)
        echo -e "${GREEN}Syncing dependencies with uv...${NC}"
        uv sync
        ;;
    
    clean)
        echo -e "${YELLOW}Cleaning environment...${NC}"
        rm -rf .venv uv.lock
        echo -e "${GREEN}Environment cleaned. Run 'uv sync' to reinstall.${NC}"
        ;;
    
    help|*)
        echo -e "${BLUE}Usage:${NC}"
        echo -e "${BLUE}  ./scripts/run dev         # Start dev server${NC}"
        echo -e "${BLUE}  ./scripts/run tests       # Run tests${NC}"
        echo -e "${BLUE}  ./scripts/run lint        # Run linting${NC}"
        echo -e "${BLUE}  ./scripts/run format      # Format code${NC}"
        echo -e "${BLUE}  ./scripts/run sync        # Sync dependencies${NC}"
        echo -e "${BLUE}  ./scripts/run clean       # Clean environment${NC}"
        ;;
esac