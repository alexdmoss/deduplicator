#!/bin/bash

file=$1
i=0

if [[ -z $file ]] || [[ ! -f $file ]]; then
	echo "No valid file supplied"
	exit 1
fi

echo "Running this script will delete all files listed in $file. Are you sure?"

read -r input

if [[ $input == "Y" ]] || [[ $input == "y" ]]; then
  while read -r line; do
    if [[ $line != "" ]]; then
      delete=$(echo "${line}" | awk -F, '{print $1}')
      if [[ -f "${delete}" ]]; then
        rm "${delete}"
        i=$(expr $i + 1)
      fi
    fi
  done < "${file}"
  echo "$i files deleted"
fi