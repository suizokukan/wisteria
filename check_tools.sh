#!/usr/bin/env bash

VERSION="check_tools.sh v.3/2021-08-26"

# ---- --help ----------------------------------------------------------------
if [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    echo "$VERSION"
    echo "check_tools.sh : show external tools versions."
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

echo "* about poetry:"
poetry --version
echo "* about shellcheck:"
shellcheck --version
echo "* about pycodestyle:"
pycodestyle --version
echo "* about pylint:"
pylint --version
echo "* about pipdeptree:"
pipdeptree --version
echo "* about pimydoc:"
pimydoc --version
echo "* about readmemd2txt:"
readmemd2txt --version

exit 0
