#!/bin/bash

if [ "$(uname -o)x" == "Cygwinx" ] ; then
    function os_path {
        cygpath -w "${1}"
    }
else
    function os_path {
        echo "${1}"
    }
fi
