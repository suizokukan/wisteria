#!/usr/bin/env bash

# (pimydoc)script utilities : create_demonstration_reports.sh

VERSION="create_demonstration_reports.sh v.3/2022-04-08"

# ---- --help ----------------------------------------------------------------
if [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    echo "$VERSION"
    echo ""
    echo "create_demonstration_reports.sh : create demonstration reports in demonstration_reports/"
    echo ""
    echo "No argument."    
    echo "You may also use:"
    echo "-h / --help   : see this message."
    echo "-v / --version: see version string."
    exit 255
elif [[ $1 = "--version" ]] || [[ $1 = "-v" ]]; then
    echo "$VERSION"
    exit 255
fi

# ==== REAL WORK =============================================================
echo "... filling demonstration_reports/1"
rm -rf demonstration_reports/1/*
poetry run bin/wisteria --cmp="pickle" --report="create_demonstration_report" --filter="data:oktrans_only" --output="console;reportfile/w=demonstration_reports/1/report.txt" --exportreport="md=demonstration_report.md"

echo "... filling demonstration_reports/2"
rm -rf demonstration_reports/2/*
poetry run bin/wisteria --cmp="all" --report="create_demonstration_report" --filter="data:oktrans_only" --output="console;reportfile/w=demonstration_reports/2/report.txt" --exportreport="md=demonstration_report.md"

echo "... filling demonstration_reports/3"
rm -rf demonstration_reports/3/*
poetry run bin/wisteria --cfgfile="demonstration_reports/wisteria2.ini" --cmp="all(ini)" --report="titles;A0;B3" --output="reportfile/w=demonstration_reports/3/report.txt" --exportreport="md=demonstration_report.md"
