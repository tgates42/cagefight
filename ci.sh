#!/bin/bash

set -e
set -x

BASEDIR=$(dirname $(readlink -f "$0"))
. ${BASEDIR}/build.sh
. ${BASEDIR}/unittest.sh
