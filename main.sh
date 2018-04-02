#!/bin/bash

set -e
set -x

BASEDIR=$(dirname $(readlink -f "$0"))
. ${BASEDIR}/build.sh
. ${BASEDIR}/env.sh

if [ ! -d ${BASEDIR}/var/out ] ; then
    mkdir ${BASEDIR}/var/out
fi
CONTID=$(docker create -t cagefightsrc:latest)
docker start "${CONTID}"
docker exec "${CONTID}" /usr/bin/python /src/coordinatecagefight.py
docker cp "${CONTID}:/var/out/run.sh" "$(os_path ${BASEDIR}/var/out/run.sh)"
docker stop "${CONTID}"
docker rm "${CONTID}"
. ${BASEDIR}/var/out/run.sh
