#!/usr/bin/env bash

# (pimydoc)script utilities : err_codes.sh

VERSION="err_codes.sh v.1/2021-09-25"

# ---- minimal/maximal indexes searched in WARNINGID$integer/ERRORID$integer strings
min_index=0
max_index=50

# ---- --help ----------------------------------------------------------------
if [[ $# -eq 0 ]] || [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    echo "$VERSION"
    echo ""
    echo "err_codes.sh : search ERRORID/WARNINGID strings"
    echo "argument:"
    echo "  * --list  : show all known err codes."
    echo "  * '001' : search 'WARNINGID001' and 'ERRORID001' strings."
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

if [ "$1" = "--list" ]
then
    for (( index=min_index; index<=max_index; index++ ))
    do
        str_index='ERRORID'$(printf "%03g" "$index")
        echo "→ ""$str_index"" :"
        ./codesearch.py "$str_index" --exclude="./*.py;./*.md;./*.sh;tests/*"

        str_index='WARNINGID'$(printf "%03g" "$index")
        echo "→ ""$str_index"" :"
        ./codesearch.py "$str_index" --exclude="./*.py;./*.md;./*.sh;tests/*"        
    done
    exit 255
fi

str_index='ERRORID'$(printf "%03g" "$1")
./codesearch.py "$str_index" --exclude="./*.py;./*.md;./*.sh;tests/*"

str_index='WARNINGID'$(printf "%03g" "$1")
./codesearch.py "$str_index" --exclude="./*.py;./*.md;./*.sh;tests/*"

exit 0
