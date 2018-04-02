#!/bin/bash

set -e
set -x

BASEDIR=$(dirname $(readlink -f "$0"))
. ${BASEDIR}/build.sh
. ${BASEDIR}/env.sh

if [ ! -d ${BASEDIR}/var/out ] ; then
    mkdir ${BASEDIR}/var/out
fi
docker run -v "$(os_path ${BASEDIR}/var/out)":/var/out -t cagefightsrc:latest \
    python /src/maincagefight.py --all
