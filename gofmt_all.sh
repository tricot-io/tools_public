#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

# Runs gofmt on all non-generated files. Suggested arguments: -s (to simplify), and -w (to modify
# files) or -d (to report diffs).
find . -name '*.go' | \
    xargs awk \
        'FNR > 3 || /Code generated .* DO NOT EDIT\./ {nextfile}; {print FILENAME; nextfile}' | \
    xargs gofmt $*
