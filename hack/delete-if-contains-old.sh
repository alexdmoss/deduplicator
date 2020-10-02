#!/usr/bin/env bash

while read line; do
  if [[ $(echo $line | grep -c '/OLD/') -gt 0 ]]; then
    echo "DELETING ::: ${line}"
    rm "${line}"
  fi
done < output.txt
