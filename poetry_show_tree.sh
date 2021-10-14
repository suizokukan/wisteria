#!/usr/bin/env bash

VERSION="poetry_show_tree.sh v.7/2021-10-14"

# ---- --help ----------------------------------------------------------------
if [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    echo "$VERSION"
    echo "This script is a wrap around '$ poetry show --tree --all', the result"
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
#     $ poetry show --tree --all| _poetry_show_tree.md
#
#  ... ?
#  Because the output colors are not kept; the output is printed in one color.
#
poetry show --tree --all
poetry show --tree --all > _tmp_poetry_show_tree.md

# is the file _tmp_poetry_show_tree.md empty ?
if ! grep -q '[^[:space:]]' _tmp_poetry_show_tree.md; then
    rm _tmp_poetry_show_tree.md
    
    echo "Result of a call to " > poetry_show_tree.md
    { echo "";
      echo "   $ poetry show --tree --all";
      echo "";
      echo "----";
      echo "";
      echo "    EMPTY RESULT: NO DEPENDENCY";
      echo "";} >> poetry_show_tree.md

    echo "(NO RESULT)"
else
    echo "Result of a call to " > poetry_show_tree.md
    # No way for me to avoid the following warning:
    #   SC2129: Consider using { cmd1; cmd2; } >> file instead of individual redirects.
    #
    # shellcheck disable=SC2129
    { echo "";
      echo "   $ poetry show --tree --all";
      echo "";
      echo "----";
      echo "";
      echo "\`\`\`";} >> poetry_show_tree.md
    cat _tmp_poetry_show_tree.md >> poetry_show_tree.md
      echo "\`\`\`" >> poetry_show_tree.md
 
    rm _tmp_poetry_show_tree.md
fi

exit 0
