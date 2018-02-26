#!/bin/bash

set -e
set -x

BASEDIR=$(dirname $(readlink -f "$0"))
echo "${BASEDIR}"

docker build -t cagefightbase:latest -f Dockerfile.cagefightbase .
docker build -t cagefightsrc:latest -f Dockerfile.cagefightsrc .
docker run -t cagefightsrc:latest /usr/local/bin/nosetests --exe /src
