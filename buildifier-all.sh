#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

# Runs buildifier on all non-generated Bazel files in the current directory and its subdirectories.

find . -name 'BUILD' -o -name 'BUILD.bazel' -o -name 'WORKSPACE' -o -name '*.bzl' | \
    xargs -r awk \
        'FNR > 3 || /Code generated .* DO NOT EDIT\./ {nextfile}; {print FILENAME; nextfile}' | \
    xargs -r buildifier $*
