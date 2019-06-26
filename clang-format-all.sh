#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

# Runs clang-format on all non-generated C and C++ files in the current directory and its
# subdirectories.
#
# Suggested arguments:
#   -i (to modify files)

set -e

if which clang-format-7 &> /dev/null; then
  CLANG_FORMAT=clang-format-7
else
  CLANG_FORMAT=clang-format
fi

find . \( -iname '*.c' -o -iname '*.cc' -o -iname '*.cpp' -o -iname '*.h' -o -iname '*.hh' -o \
        -iname '*.hpp' \) -print0 | \
    xargs -r0 gawk -vORS='\0' \
        'FNR > 3 || /Code generated .* DO NOT EDIT\./ {nextfile}; {print FILENAME; nextfile}' | \
    xargs -r0 "$CLANG_FORMAT" $*
