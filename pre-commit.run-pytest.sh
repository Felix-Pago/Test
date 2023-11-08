#!/bin/sh
RED='\033[0;31m'
# shellcheck disable=SC2034
NC='\033[0m' # No Color

test_results=$(script -q /dev/null pytest testing/app/**/*.py  -v --tb=no)
if [ $? -eq 1 ]; then
   # shellcheck disable=SC2059
   printf "${RED}CANNOT COMMIT, PYTEST FAILED\n\nPYTEST RESULTS:\n"
   echo "$test_results"
   exit 1
fi


# NO ERRORS
exit 0
