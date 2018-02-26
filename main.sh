#!/bin/bash

set -e
set -x

BASEDIR=$(dirname $(readlink -f "$0"))
docker run -t cagefightsrc:latest
