#!/bin/bash

set -eu

SCRIPT_ROOT="$(dirname $(realpath ${BASH_SOURCE[0]}))"
CC=clang

#-- Logging

log::echo() {
  echo "$@"
}

log::info() {
  local prefix="info: "
  local newline="\n" 
  local maybe_option="${2:-}"

  if [[ $maybe_option == *">"* ]]; then
    newline=""
  fi
  if [[ $maybe_option == *"-"* ]]; then
    prefix=""
  fi

  printf "${prefix}$1${newline}"
}

log::warn() {
  echo "warning: $@"
}

log::error() {
  echo "error: $@"
}

#--

__prompt_cur_depth=0

prompt::print_head() {
  for i in $(seq 1 $__prompt_cur_depth); do
    printf "╰─"
  done
  printf "> "
}

#--

arr_incls=()
arr_

log::echo "C REPL (version $(date -r $0 +%d-%m-%Y))"

while true; do
  prompt::print_head
  IFS='\n' read -r line
  echo "$line"
done
