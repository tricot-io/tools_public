#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

# Runs clang-format on all non-generated C++ files in the current directory and its subdirectories.
#
# Suggested arguments:
#   -i (to modify files)

if which clang-format-7 &> /dev/null; then
  CLANG_FORMAT=clang-format-7
else
  CLANG_FORMAT=clang-format
fi

find . -name '*.cc' -o -name '*.h' | \
    xargs awk -r \
        'FNR > 3 || /Code generated .* DO NOT EDIT\./ {nextfile}; {print FILENAME; nextfile}' | \
    xargs -r "$CLANG_FORMAT" $*
