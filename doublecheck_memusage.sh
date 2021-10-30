#!/usr/bin/env bash

# memory usage: doublecheck_memusage.sh

VERSION="doublecheck_memusage.sh v.1/2021-10-10"

# ---- --help ----------------------------------------------------------------
if [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    echo "$VERSION"
    echo ""
    echo "doublecheck_memusage.sh : check the memory usage by wisteria"
    echo "no argument."
    echo ""    
    echo "You may use:"
    echo "-h / --help   : see this message."
    echo "-v / --version: see version string."
    exit 255
elif [[ $1 = "--version" ]] || [[ $1 = "-v" ]]; then
    echo "$VERSION"
    exit 255
fi

# ==== REAL WORK =============================================================
echo "It takes a long time to run this script, so be patient!"

echo "*   --help: minimal memory usage"
valgrind -q --tool=massif --pages-as-heap=yes --massif-out-file=massif.out python3.9 ./bin/wisteria --help --verbosity=0 &> /dev/null; grep mem_heap_B massif.out | sed -e 's/mem_heap_B=\(.*\)/\1/' | sort -g | tail -n 1 | awk '{print $1" bytes"}'

echo "*   --checkup: reduced memory usage"
valgrind -q --tool=massif --pages-as-heap=yes --massif-out-file=massif.out python3.9 ./bin/wisteria --checkup --mute; grep mem_heap_B massif.out | sed -e 's/mem_heap_B=\(.*\)/\1/' | sort -g | tail -n 1 | awk '{print $1" bytes"}'

echo "*   --cmp='iaswn vs pyyaml' --memoveruse=none: normal memory usage"
valgrind -q --tool=massif --pages-as-heap=yes --massif-out-file=massif.out python3.9 ./bin/wisteria --cmp="iaswn vs pyyaml(all)" --mute --memoveruse=none; grep mem_heap_B massif.out | sed -e 's/mem_heap_B=\(.*\)/\1/' | sort -g | tail -n 1 | awk '{print $1" bytes"}'

echo "*   --cmp='iaswn vs pyyaml' --memoveruse=Python: extra memory usage (Python)"
valgrind -q --tool=massif --pages-as-heap=yes --massif-out-file=massif.out python3.9 ./bin/wisteria --cmp="iaswn vs pyyaml(all)" --mute --memoveruse="Python"; grep mem_heap_B massif.out | sed -e 's/mem_heap_B=\(.*\)/\1/' | sort -g | tail -n 1 | awk '{print $1" bytes"}'

echo "*   --cmp='iaswn vs pyyaml' --memoveruse=C++: extra memory usage (C++)"
valgrind -q --tool=massif --pages-as-heap=yes --massif-out-file=massif.out python3.9 ./bin/wisteria --cmp="iaswn vs pyyaml(all)" --mute --memoveruse="C++"; grep mem_heap_B massif.out | sed -e 's/mem_heap_B=\(.*\)/\1/' | sort -g | tail -n 1 | awk '{print $1" bytes"}'

echo "*   --cmp='iaswn vs pyyaml' --memoveruse=Python/C++: extra memory usage (Python+C++)"
valgrind -q --tool=massif --pages-as-heap=yes --massif-out-file=massif.out python3.9 ./bin/wisteria --cmp="iaswn vs pyyaml(all)" --mute --memoveruse="Python/C++"; grep mem_heap_B massif.out | sed -e 's/mem_heap_B=\(.*\)/\1/' | sort -g | tail -n 1 | awk '{print $1" bytes"}'
