#!/usr/bin/env bash
set -e

TEST_TYPE="integration"
PYTHON_BIN="/usr/bin/python3"
THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1 && pwd)"

usage() {
    echo "run-tests.sh -p=PYTHON_BIN -t=TEST_TYPE"
    exit 1
}

check_args() {
    for i in "$@"; do
        case $i in
            -t=* | --test-type=*)
                TEST_TYPE="${i#*=}"
                ;;
            -p=* | --python-bin=*)
                PYTHON_BIN="${i#*=}"
                ;;
            *)
                usage
                ;;
        esac
    done
}

check_args $@

# Prepare the execution virtualenv
virtualenv --python ${PYTHON_BIN} ${THIS_DIR}/venv
source ${THIS_DIR}/venv/bin/activate
trap "deactivate" EXIT
if [ -f ${THIS_DIR}/requirements-dev.txt ]; then
    pip install -r ${THIS_DIR}/requirements-dev.txt --no-deps
fi

# Execute the specified test suite
python -m unittest discover --verbose --catch --start-directory ${THIS_DIR}/tests/${TEST_TYPE}
if [ $? -ne 0 ]; then
    exit 1
fi
