#!/bin/bash

file=$1
rm -f /tmp/dedupe.txt
i=0

if [[ -z $file ]] || [[ ! -f $file ]]; then
	echo "No valid file supplied"
	exit 1
fi

echo "Running this script will delete files from alexd/ where they exist in gdrive/ (using ${file}). Are you sure?"

# read input
input=y

if [[ $input == "Y" ]] || [[ $input == "y" ]]; then

  while read line; do
    if [[ $line != "" ]]; then
      if [[ -f "$line" ]]; then
        if [[ $(echo "${line}" | grep -c '/alexd/') -gt 0 ]]; then
          gdrive_equiv=$(echo "${line}" | sed 's#/alexd/#/gdrive/#')
          if [[ $(grep -c "${gdrive_equiv}" "${file}") -gt 0 ]]; then
            echo "[INFO] ${line} is in gdrive & alexd"
            echo "${line}" >> /tmp/dedupe.txt
          fi
        fi
      fi
    fi
  done < $file

  while read line; do
    file_to_delete=$(grep "${line}" "${file}" | grep alexd)
    echo "[DELETING] ${file_to_delete}"
    rm "$line"
    i=$(expr $i + 1)
  done < /tmp/dedupe.txt

  echo "$i files deleted"

fi