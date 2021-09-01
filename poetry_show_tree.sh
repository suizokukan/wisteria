#!/usr/bin/env bash

VERSION="poetry_show_tree.sh v.5/2021-08-31"

# ---- --help ----------------------------------------------------------------
if [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    echo "$VERSION"
    echo "This script is a wrap around '$ poetry show --tree', the result"
    echo "being printed on the screen and written into poetry_show_tree.md ."
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
#
#  Why not...
#     $ poetry show --tree | _poetry_show_tree.md
#
#  ... ?
#  Because the output colors are not kept; the output is printed in one color.
#
poetry show --tree
poetry show --tree > _tmp_poetry_show_tree.md

# is the file _tmp_poetry_show_tree.md empty ?
if ! grep -q '[^[:space:]]' _tmp_poetry_show_tree.md; then
    rm _tmp_poetry_show_tree.md
    
    echo "Result of a call to " > poetry_show_tree.md
    { echo "";
      echo "   $ poetry show --tree";
      echo "";
      echo "----";
      echo "";
      echo "    EMPTY RESULT: NO DEPENDENCY";
      echo "";} >> poetry_show_tree.md

    echo "(NO RESULT)"
else
    echo "Result of a call to " > poetry_show_tree.md
    { echo "";
      echo "   $ poetry show --tree";
      echo "";
      echo "----";
      echo "";} >> poetry_show_tree.md
    cat _tmp_poetry_show_tree.md >> poetry_show_tree.md

    rm _tmp_poetry_show_tree.md
fi

exit 0
