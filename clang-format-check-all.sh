#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

# Checks that files are clang-format-ed.

set -e

if ("$(dirname "$BASH_SOURCE")/clang-format-all.sh" -output-replacements-xml | \
        grep -q '<replacement ') &> /dev/null; then
    echo "Found clang-format errors"
    exit 1
fi
exit 0
