#!/bin/bash

set -e
set -x

BASEDIR=$(dirname $(readlink -f "$0"))
docker build -t ffmpegbase:latest -f Dockerfile.ffmpegbase .
docker build -t cagefightbase:latest -f Dockerfile.cagefightbase .
docker build -t cagefightsrc:latest -f Dockerfile.cagefightsrc .
docker build -t cagefighterbasic:latest -f Dockerfile.cagefighterbasic .
