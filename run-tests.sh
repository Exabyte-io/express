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

SOURCE="${BASH_SOURCE[0]}"
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

for LIB in esse; do
    cd /stack/lib/${LIB}
    git checkout dev
    git pull --all
    cd -
done

virtualenv ${DIR}/venv
source ${DIR}/venv/bin/activate
pip install -r ${DIR}/requirements.txt

export PYTHONPATH=${DIR}:${PYTHONPATH}
CMD="python -m unittest discover -v -c -s"
${CMD} ${DIR}/tests/unit && ${CMD} ${DIR}/tests/integration
