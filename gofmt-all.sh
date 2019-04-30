#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

# Runs gofmt on all non-generated Go files in the current directory and its subdirectories.
#
# Suggested arguments:
#   -s (to simplify)
#   -w (to modify files) or -d (to report diffs)

find . -name '*.go' | \
    xargs awk \
        'FNR > 3 || /Code generated .* DO NOT EDIT\./ {nextfile}; {print FILENAME; nextfile}' | \
    xargs gofmt $*
