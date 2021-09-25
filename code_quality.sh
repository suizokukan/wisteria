#!/usr/bin/env bash

VERSION="poetry_show_tree.sh v.4/2021-08-25"

# ---- --help ----------------------------------------------------------------
if [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    echo "$VERSION"
    echo "code_quality.sh : check code quality."
    echo ""
    echo "No argument required but you may use:"
    echo "-h / --help   : see this message."
    echo "-v / --version: see version string."
    exit 255
elif [[ $1 = "--version" ]] || [[ $1 = "-v" ]]; then
    echo "$VERSION"
    exit 255
fi

# ==== REAL WORK =============================================================
echo "* about shellcheck:"
shellcheck --version
echo "* about pycodestyle:"
pycodestyle --version
echo "* about pylint:"
pylint --version

echo

echo "=== pycodestyle . --max-line-length=100 ==="
pycodestyle . --max-line-length=100
echo "=== pylint ./*.py ==="
pylint ./*.py
echo "=== pylint wisteria/*.py ==="
pylint wisteria/*.py
echo "=== wisteria/*.py ==="
pylint tests/*.py
echo "=== shellcheck ./*.sh ==="
shellcheck ./*.sh
exit 0
