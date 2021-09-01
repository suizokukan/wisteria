#!/usr/bin/env bash

VERSION="docdef.sh v.2/2021-08-31"

# ---- --help ----------------------------------------------------------------
if [[ $# -eq 0 ]] || [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    echo "$VERSION"
    echo ""
    echo "docdef.sh : show DOCDEF definitions/confer(s)"
    echo ""
    echo "This script assumes that you have added in your code documentation definitions "
    echo "like this one: (syntax being DOCREF + 3 digits)"
    echo "  # DOCREF001"
    echo "  # This is a definition for reference 001."
    echo ""
    echo "This script also assumes that you have added in your code references to "
    echo "documentation definitions like this one: (syntax being confer DOCREF + 3 digits)"
    echo "  # For more details, confer DOCREF001"
    echo "  # This is a definition for reference 001."
    echo ""
    echo "arguments:"
    echo "  * '004'        : definition of 'DOCDEF004' (def. searched everywhere, not only in the code subdirectory"
    echo "  * --defslist   : show all definitions number (e.g. DOCDEF004) in the code subdirectory"
    echo "  * --defslist2  : show all definitions number (e.g. DOCDEF004) and confer-s (e.g. confer DOCDEF004) in the code subdirectory"
    echo "  * --list       : show all occurences of the 'DOCDEF' string in the code subdirectory"
    echo ""
    echo "You may also use:"
    echo "-h / --help   : see this message."
    echo "-v / --version: see version string."
    exit 255
elif [[ $1 = "--version" ]] || [[ $1 = "-v" ]]; then
    echo "$VERSION"
    exit 255
fi

# ==== REAL WORK =============================================================

# ---- minimal/maximal indexes searched in DOCDEF$integer strings ------------
min_index=1
max_index=20

# ==== REAL WORK =============================================================

# ---- --defslist ------------------------------------------------------------
if [ "$1" = "--defslist" ]
then
    for (( index=min_index; index<=max_index; index++ ))
    do
        str_index="definition of DOCDEF"$(printf "%03g" """$index""")

        echo "→ '$str_index' :"
        ./codesearch.py --codesubdirectoryonly "$str_index"
    done
    exit 0
fi

# ---- --defslist2 -----------------------------------------------------------
if [ "$1" = "--defslist2" ]
then
    for (( index=min_index; index<=max_index; index++ ))
    do
        str_index="definition of DOCDEF"$(printf "%03g" """$index""")

        echo "→ '$str_index' :"
        ./codesearch.py "$str_index"

        # "onfer" and not "confer": it's not an error: we want to get "Confer DOCDEF..." as well as "confer DOCDEF..."
        str_index="onfer DOCDEF"$(printf "%03g" """$index""")
        ./codesearch.py --codesubdirectoryonly "$str_index"

    done
    exit 0
fi

# ---- --list ----------------------------------------------------------------
if [ "$1" = "--list" ]
then
    for (( index=min_index; index<=max_index; index++ ))
    do
        str_index="DOCDEF"$(printf "%03g" """$index""")

        echo "→ '$str_index' :"
        ./codesearch.py --codesubdirectoryonly "$str_index"
    done
    exit 0
fi

# ---- substring to be find --------------------------------------------------
find . -name "*.py" -exec grep -A 25 -rHn --color "definition of DOCDEF$1" {} \;
exit 0
