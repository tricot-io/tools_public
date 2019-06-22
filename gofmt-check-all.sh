#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

# Checks that files are buildifier-ed.

set -e

ERRORS=$("$(dirname "$BASH_SOURCE")/gofmt-all.sh" -s -l)
if [[ -z "$ERRORS" ]]; then
    exit 0
fi

echo "gofmt errors found in:"
echo "$ERRORS"
exit 1
