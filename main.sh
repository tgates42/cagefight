#!/bin/bash

set -e
set -x

BASEDIR=$(dirname $(readlink -f "$0"))
. ${BASEDIR}/build.sh
if [ ! -d ${BASEDIR}/var/out ] ; then
    mkdir ${BASEDIR}/var/out
fi
docker run -v "$(cygpath -w ${BASEDIR}/var/out)":/var/out -t cagefightsrc:latest \
    python /src/cagefight/cagefightmain.py
