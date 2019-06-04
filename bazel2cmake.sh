#!/bin/bash
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

# Builds and runs bazel2cmake (from tricot-io/bazel2x).

B2X_REV="HEAD"

while getopts ":hr:c:o:" OPT; do
    case "${OPT}" in
        h)
            echo "Usage: $0 [-h] [-r <bazel2x rev>] [-c <cfg file>] [-o <out dir>] <workspace dir>"
            echo
            echo "    -h: help"
            echo "    -r <bazel2x rev>: bazel2x revision (or tag)"
            echo "    -c <cfg file>: configuration file"
            echo "    -o <out dir>: output directory"
            exit 0
            ;;
        r)
            B2X_REV="${OPTARG}"
            ;;
        c)
            CFG_FILE="${OPTARG}"
            ;;
        o)
            OUT_DIR="${OPTARG}"
            ;;
        \?)
            echo "Error: invalid option -${OPTARG}"
            exit 1
            ;;
        :)
            echo "Error: option -${OPTARG} requires an argument"
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if [[ $# -ne 1 ]]; then
    echo "Error: workspace directory argument required"
    exit 1
fi
WORKSPACE_DIR="$1"

echo "Building bazel2cmake ..."

B2X_DIR="$(mktemp -d)"
function at_exit {
    rm -rf "${B2X_DIR}"
}
trap at_exit EXIT

BAZEL2CMAKE="${B2X_DIR}/bazel2cmake"

(
    cd "${B2X_DIR}"
    set -x
    git clone -n -q -- https://github.com/tricot-io/bazel2x bazel2x
    cd bazel2x
    git checkout "${B2X_REV}"
    go build -o "${BAZEL2CMAKE}" ./cmd/bazel2cmake
)

echo "Running bazel2cmake ..."
BAZEL2CMAKE_ARGS=()
if [[ -n "${CFG_FILE}" ]]; then
    BAZEL2CMAKE_ARGS+=("-config_file" "${CFG_FILE}")
fi
if [[ -n "${OUT_DIR}" ]]; then
    BAZEL2CMAKE_ARGS+=("-out_dir" "${OUT_DIR}")
fi
BAZEL2CMAKE_ARGS+=("${WORKSPACE_DIR}")
(set -x; "${BAZEL2CMAKE}" "${BAZEL2CMAKE_ARGS[@]}")
