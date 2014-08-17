#!/bin/bash
#

exec_dir=/etc/simple.d/monitor

read args

if [[ "$1" ]]; then
  echo "$args" | nc $1 3333
  exit 0
fi

for a in ${args//|/ }; do
  cmd=$exec_dir/${a//%/ }
  cmd=${cmd//../}
  if [[ -x ${cmd/ *} ]]; then
    result=$($cmd)
    code=$?
    echo $result
  fi
done
