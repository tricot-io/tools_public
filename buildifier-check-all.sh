#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

# Checks that files are buildifier-ed.

set -e

"$(dirname "$BASH_SOURCE")/buildifier-all.sh" -mode check
