#!/usr/bin/env bash

set -e

# Ensure current path is project root
cd "$(dirname "$0")/../"

git clone https://github.com/sigridjineth/rust-racingcar /tmp/rust-racingcar

QDRANT_PATH=/tmp/qdrant bash -x tools/index_qdrant.sh /tmp/rust-racingcar

rm -rf /tmp/qdrant

