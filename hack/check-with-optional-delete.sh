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

    delete=N

    echo "Opening for line ${i}"
    
    file1=$(echo "${line}" | awk -F\| '{print $1}')
    file2=$(echo "${line}" | awk -F\| '{print $3}')

    if [[ -f ${file1} ]] && [[ -f ${file2} ]]; then

        win_file1=$(echo "${file1}" | sed 's#/mnt/c/#c:/#')
        win_file2=$(echo "${file2}" | sed 's#/mnt/c/#c:/#')

        wslview "${win_file1}" &
        sleep 0.5
        wslview "${win_file2}" &
        sleep 0.5

        echo "Delete 1 or 2?"
        read -r delete

        if [[ $delete == "1" ]]; then
            echo "Deleting ${file1}"
            rm "${file1}"
        elif [[ $delete == "2" ]]; then
            echo "Deleting ${file2}"
            rm "${file2}"
        fi
        
    fi

    i=$((i + 1))

done

IFS=$IFS_BAK
IFS_BAK=
