#!/usr/bin/env bash
set -euoE pipefail

# Just a little hack script for me to feel a bit more confident that the python code
# has definitely matched identical photos correctly before I delete them forever.
#
# Opens all images from input file one by one from WSL (the machine with all the 
# images on it) using its default image viewer.

IFS_BAK=$IFS
IFS=$'\n'
files=$(cat "${1}")
i=1

for line in $files; do

    echo "Opening for line ${i}"
    
    file1=$(echo "${line}" | awk -F\| '{print $1}' | sed 's#/mnt/c/#c:/#')
    file2=$(echo "${line}" | awk -F\| '{print $3}' | sed 's#/mnt/c/#c:/#')

    wslview "${file1}" &
    sleep 0.5
    wslview "${file2}" &
    sleep 0.5

    i=$((i + 1))

done

IFS=$IFS_BAK
IFS_BAK=
