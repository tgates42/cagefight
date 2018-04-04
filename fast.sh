#!/bin/bash

set -e
set -x

BASEDIR=$(dirname $(readlink -f "$0"))
. ${BASEDIR}/build.sh
. ${BASEDIR}/env.sh

if [ ! -d ${BASEDIR}/var/out ] ; then
    mkdir ${BASEDIR}/var/out
fi
CONTID=$(docker create -t cagefightsrc:latest sleep 600)
docker start "${CONTID}"
docker exec "${CONTID}" /usr/bin/python /src/maincagefight.py --all
docker cp "${CONTID}:/var/out/output.mp4" "$(os_path ${BASEDIR}/var/out/output.mp4)"
docker cp "${CONTID}:/var/out/results.csv" "$(os_path ${BASEDIR}/var/out/results.csv)"
docker stop "${CONTID}"
docker rm "${CONTID}"
