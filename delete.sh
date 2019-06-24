#!/bin/bash

file=$1
i=0

if [[ -z $file ]] || [[ ! -f $file ]]; then
	echo "No valid file supplied"
	exit 1
fi

while read line; do
  if [[ $line != "" ]]; then
    if [[ -f "$line" ]]; then
      rm "$line"
      i=$(expr $i + 1)
    fi
  fi
done < $file

echo "$i files deleted"

