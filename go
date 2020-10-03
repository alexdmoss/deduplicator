#!/usr/bin/env bash
set -Eeuo pipefail

if [[ -z ${IMAGE_NAME:-} ]]; then
  IMAGE_NAME=deduplicator
fi 

function help() {
  echo -e "Usage: go <command>"
  echo -e
  echo -e "    help                 Print this help"
  echo -e "    run                  Run locally from source"
  echo -e "    run-docker           Run already-built docker image"
  echo -e "    build                Build Docker image (won't push anywhere)"
  echo -e "    test                 Run local unit tests and linting"
  echo -e "    watch-tests          Watch pytest run for faster feedback"
  echo -e 
  exit 0
}


function run() {
  pipenv run python3 main.py "$@"
}

function watch-tests() {
  pipenv run ptw
}

function test() {
  pipenv run flake8 .
  # pipenv run pytype --keep-going .
  pipenv run pytest -s -v
}

function build() {
  docker build --tag ${IMAGE_NAME}:latest .
}

function run-docker() {
  docker run -v ${PWD}/output:/app/output ${IMAGE_NAME}:latest "$@"
}

function ctrl_c() {
    if [ ! -z ${PID:-} ]; then
        kill ${PID}
    fi
    exit 1
}

trap ctrl_c INT

if [[ ${1:-} =~ ^(help|run|run-docker|build|test|watch-tests)$ ]]; then
  COMMAND=${1}
  shift
  $COMMAND "$@"
else
  help
  exit 1
fi
