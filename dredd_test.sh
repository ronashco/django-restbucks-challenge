#!/usr/bin/env bash

usage() { echo "Usage: $0 [-s service-name <e.g. accounting>] [-f compose.yml <test-compose.yml>] [-w wait-timeout <30>]" 1>&2; exit 1; }

OPTS=`getopt -o hbdfws: --long help,build,delete,file:,wait:,service: -n 'dredd_test' -- "$@"`

if [ $? != 0 ] ; then usage; exit 1 ; fi

eval set -- "$OPTS"

. ./test.conf.env #read config file and load defaults

if [ $? != 0 ] ; then echo "No config file found..."; exit 1 ; fi

while true; do
  case "$1" in
    -f | --file ) COMPOSE="$2"; shift 2 ;;
    -w | --wait ) WAIT_TIME="$2"; shift 2 ;;
    -s | --service ) SERVICE="$2"; shift 2 ;;
    -b | --build ) BUILD=--build; shift ;;
    -d | --delete ) DELETE=true; shift ;;
    -h | --help ) usage; shift ;;
    -- ) shift; break ;;
    * ) usage; break ;;
  esac
done

WD=$(pwd)

trap ctrl_c INT

function ctrl_c() {
        docker-compose -f $WD/${COMPOSE} down
        exit 1
}


printf '\x1B[34m' # print blue
printf "Starting dredd test with the following configuration"
printf '\n\x1B[0m' # print normal

printf '\x1B[32m\n' # print green
printf "\tService name: $SERVICE \n"
printf "\tCOMPOSE: $COMPOSE \n"
printf "\tWAIT_TIME: $WAIT_TIME \n"
printf "\tAPPS: ${APPS[*]} \n"
printf '\n\x1B[0m' # print normal

printf '\x1B[34m' # print blue
printf 'Starting containers'
printf '\n\x1B[0m' # print normal
docker-compose -f ${COMPOSE} up $BUILD -d

# health check
printf '\x1B[34m' # print blue
printf 'Waiting for app'
COUNTER=0
until curl -sf http://127.0.0.1:8080/$SERVICE/watchman/ > /dev/null; do
  sleep 1
  COUNTER=$((COUNTER + 1))
  if [ "$COUNTER" -gt "$WAIT_TIME" ]
  then
    printf '\x1B[31m\n' # print red
    printf 'Wait time out!'
    printf '\n\x1B[0m' # print normal
    docker-compose -f ${COMPOSE} down
    exit 1
  fi

  printf '.'
done
printf '\x1B[32m\n' # print green
printf 'App is ready!'
printf '\n\x1B[0m' # print normal

# dredd test
printf '\x1B[34m' # print blue
printf 'Starting tests...'
printf '\n\x1B[0m' # print normal

for i in ${APPS[@]}; do
        cd ${i}/doc
        pwd
        dredd --hookfiles hooks.py
        exitcode=$?
        rst=$((rst + exitcode))
        cd ../..
done
if [ $DELETE ]
then
    docker-compose -f ${COMPOSE} down
fi
exit ${rst} # exit with dredd exit code
