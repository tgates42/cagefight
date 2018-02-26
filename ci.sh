#!/bin/bash

set -e
set -x

BASEDIR=$(dirname $(readlink -f "$0"))
echo "${BASEDIR}"

docker build -t cagefight:latest .
docker run -t cagefight:latest
