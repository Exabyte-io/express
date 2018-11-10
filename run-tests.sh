#!/bin/bash

# ---------------------------------------------------------- #
#  Written @ Exabyte.io                                      #
# ---------------------------------------------------------- #
#                                                            #
#  Wrapper script to run repo-specific tests.                #
#  Non-zero exit code is returned on test failure.           #
#                                                            #
#    0. Set necessary environment variables                  #
#    1. Run tests through python unittests module            #
#                                                            #
# ---------------------------------------------------------- #

TEST_TYPE="unit"
PYTHON_ENV="/tmp/express"
SRC="/stack/lib/express"

# ------------------------------------------------------------- #
#                         SETUP                                 #
# ------------------------------------------------------------- #


usage () {
    echo "run-tests.sh -t=TEST_TYPE"
    exit 1
}

check_args () {
    for i in "$@"
    do
        case $i in
            -t=*|--test-type=*)
                TEST_TYPE="${i#*=}"
            ;;
            -s=*|--source=*)
                SRC="${i#*=}"
            ;;
            *)
                usage
            ;;
        esac
    done
}

# ------------------------------------------------------------- #
#                       MAIN BODY                               #
# ------------------------------------------------------------- #

check_args $@

irm -rf ${PYTHON_ENV}
virtualenv ${PYTHON_ENV}

for LIB in esse; do
    cd /stack/lib/${LIB}
    git checkout dev
    git pull --all
done
cd ${SRC}

${PYTHON_ENV}/bin/pip install --process-dependency-links -r ${SRC}/requirements.txt

source ${PYTHON_ENV}/bin/activate
export PYTHONPATH=${SRC}:${PYTHONPATH}

python -m unittest discover -v -c -s ${SRC}/tests/${TEST_TYPE}
if [ $? -ne 0 ]; then
    exit 1
fi
