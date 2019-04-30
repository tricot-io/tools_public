#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

if which clang-format-7 &> /dev/null; then
  CLANG_FORMAT=clang-format-7
else
  CLANG_FORMAT=clang-format
fi

# Runs clang-format on all non-generated files. Suggested arguments: -i (to modify files).
find . -name '*.cc' -o -name '*.h' | \
    xargs awk \
        'FNR > 3 || /Code generated .* DO NOT EDIT\./ {nextfile}; {print FILENAME; nextfile}' | \
    xargs "$CLANG_FORMAT" $*
