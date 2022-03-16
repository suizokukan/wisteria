#!/usr/bin/env bash

# (pimydoc)script utilities : create_demonstration_reports.sh

VERSION="create_demonstration_reports v.1/2022-03-16"

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
rm -rf demonstration_reports/1/*
poetry run bin/wisteria --cmp="pickle" --report="glance" --filter="data:oktrans_only" --output="reportfile/w=demonstration_reports/1/report.txt" --exportreport="md=demonstration_report.md"

rm -rf demonstration_reports/2/*
poetry run bin/wisteria --cmp="all" --report="glance" --filter="data:oktrans_only" --output="reportfile/w=demonstration_reports/2/report.txt" --exportreport="md=demonstration_report.md"

rm -rf demonstration_reports/3/*
poetry run bin/wisteria --cfgfile="demonstration_reports/wisteria2.ini" --cmp="all(ini)" --report="titles;B3" --output="reportfile/w=demonstration_reports/3/report.txt" --exportreport="md=demonstration_report.md"
