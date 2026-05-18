#!/usr/bin/env bash
# ─────────────────────────────────────────────────────
#  Spectra Installer
#  curl -fsSL https://raw.githubusercontent.com/yourname/spectra/main/install.sh | bash
# ─────────────────────────────────────────────────────

set -e

PURPLE='\033[38;5;129m'
VIOLET='\033[38;5;135m'
GREEN='\033[38;5;83m'
RED='\033[38;5;196m'
GRAY='\033[38;5;245m'
BOLD='\033[1m'
RESET='\033[0m'

echo ""
echo -e "${BOLD}${PURPLE}  ⬡  Installing Spectra…${RESET}"
echo -e "${GRAY}  ─────────────────────────────────${RESET}"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}  ✗  Python 3 not found. Install it from https://python.org${RESET}"
    exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}  ✓${RESET}  Python ${PY_VERSION} found"

# Check pip
if ! command -v pip3 &>/dev/null && ! python3 -m pip --version &>/dev/null; then
    echo -e "${RED}  ✗  pip not found. Install pip first.${RESET}"
    exit 1
fi

echo -e "${GREEN}  ✓${RESET}  pip found"
echo ""
echo -e "${VIOLET}  ◈  Installing from GitHub…${RESET}"
echo ""

pip3 install git+https://github.com/yourname/spectra.git --quiet

echo ""
echo -e "${GREEN}  ✓${RESET}  ${BOLD}Spectra installed successfully!${RESET}"
echo ""
echo -e "  Run ${PURPLE}spectra${RESET} to get started."
echo -e "  Run ${PURPLE}spectra start${RESET} to start mirroring."
echo ""
