#!/usr/bin/env bash
set -e

TEST_TYPE="unit"
PYTHON_BIN="python3"
THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1 && pwd)"
VENV_NAME="venv"

usage() {
    echo "run-tests.sh -p=PYTHON_BIN -v=VENV_NAME -t=TEST_TYPE"
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
            -v=* | --venvdir=*)
                VENV_NAME="${i#*=}"
                ;;
            *)
                usage
                ;;
        esac
    done
}

check_args $@

# Prepare the execution virtualenv
virtualenv --python ${PYTHON_BIN} ${THIS_DIR}/${VENV_NAME}
source ${THIS_DIR}/${VENV_NAME}/bin/activate
trap "deactivate" EXIT
if [ -f ${THIS_DIR}/requirements-dev.txt ]; then
    pip install -r ${THIS_DIR}/requirements-dev.txt
fi

# Execute the specified test suite
coverage run -m unittest discover --verbose --catch --start-directory ${THIS_DIR}/tests/${TEST_TYPE}

# Generate the code coverage reports
coverage report
coverage html --directory htmlcov_${TEST_TYPE}
coverage xml -o coverage_${TEST_TYPE}.xml
