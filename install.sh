#!/bin/bash
# Pencil Design Agent — One-line installer
#
# Usage (from your project root):
#   curl -fsSL https://raw.githubusercontent.com/monsieur-pixeler/pencil-designer-bmad/main/install.sh | bash
#
# Or clone first:
#   git clone https://github.com/monsieur-pixeler/pencil-designer-bmad.git /tmp/pencil-designer-bmad
#   bash /tmp/pencil-designer-bmad/install.sh
#
# What it does:
#   1. Copies pencil-design/ into .claude/skills/ of the current project
#   2. Tells you how to start First Breath
#
# It does NOT modify _bmad/ config — run /pencil-design setup for that.

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_ROOT="$(pwd)"
SKILL_DEST="${PROJECT_ROOT}/.claude/skills/pencil-design"

echo ""
echo -e "${GREEN}Pencil Design Agent${NC} — installer"
echo "Installing into: ${PROJECT_ROOT}"
echo ""

# Determine source location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "${SCRIPT_DIR}/pencil-design" ]; then
    SOURCE_DIR="${SCRIPT_DIR}/pencil-design"
elif [ -d "/tmp/pencil-designer-bmad/pencil-design" ]; then
    SOURCE_DIR="/tmp/pencil-designer-bmad/pencil-design"
else
    # Clone from GitHub
    echo "Downloading from GitHub..."
    TEMP_DIR=$(mktemp -d)
    git clone --depth 1 https://github.com/monsieur-pixeler/pencil-designer-bmad.git "${TEMP_DIR}" 2>/dev/null
    SOURCE_DIR="${TEMP_DIR}/pencil-design"
    CLEANUP_TEMP=true
fi

# Check source exists
if [ ! -f "${SOURCE_DIR}/SKILL.md" ]; then
    echo -e "${RED}Error: Could not find pencil-design skill files${NC}"
    exit 1
fi

# Check if already installed
if [ -d "${SKILL_DEST}" ]; then
    echo -e "${YELLOW}Pencil is already installed at ${SKILL_DEST}${NC}"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
    rm -rf "${SKILL_DEST}"
fi

# Install
mkdir -p "${PROJECT_ROOT}/.claude/skills"
cp -R "${SOURCE_DIR}" "${SKILL_DEST}"

# Remove __pycache__ if present
find "${SKILL_DEST}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Cleanup temp if we cloned
if [ "${CLEANUP_TEMP:-false}" = true ]; then
    rm -rf "${TEMP_DIR}"
fi

# Count what was installed
FILE_COUNT=$(find "${SKILL_DEST}" -type f | wc -l | tr -d ' ')
CAP_COUNT=$(grep -c '^\| \[' "${SKILL_DEST}/assets/CAPABILITIES-template.md" 2>/dev/null || echo "17")

echo ""
echo -e "${GREEN}Installed successfully${NC}"
echo "  Location:     ${SKILL_DEST}"
echo "  Files:        ${FILE_COUNT}"
echo "  Capabilities: ${CAP_COUNT} built-in"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "  1. Start Claude Code in this project"
echo "  2. Type: /pencil-design setup        (registers with BMad config)"
echo "     — or just start designing:  \"Talk to Pencil\""
echo ""
echo "  Pencil will run First Breath automatically on the first session"
echo "  to learn about your project, design system, and preferences."
echo ""
echo "  Requirements: Pencil.dev (Desktop App or VS Code Extension)"
echo "                uv (for Python scripts)"
echo ""
