#!/usr/bin/env bash

# Supply image output file, and it will delete the second image if its 
# filesize is larger (it should be, from sort in image-results-parse.py) 

while read -r line; do

    file1=$(echo "${line}" | awk -F\| '{print $1}')
    file2=$(echo "${line}" | awk -F\| '{print $3}')
    res1=$(echo "${line}" | awk -F\| '{print $2}')
    res2=$(echo "${line}" | awk -F\| '{print $2}')

    if [[ "${file1}" != "${file2}" ]]; then

        if [[ -f "${file1}" ]] && [[ -f "${file2}" ]]; then

            filesize1=$(stat -c %s "${file1}")
            filesize2=$(stat -c %s "${file2}")

            if [[ "${filesize1}" -gt "${filesize2}" ]]; then
                echo "[INFO] All good, deleting the second file - ${file2}"
                rm "${file2}"
            else
                if [[ "${res1}" == "${res2}" ]]; then
                    echo "[INFO] Same resolution, deleting the second file - ${file2}"
                    rm "${file2}"
                else
                    echo "[WARN] ${file2} was larger than ${file1} and resolution did not match"
                fi
            fi
        else
            echo "[INFO] One of the files no longer exists"
        fi

    else
        echo "[ERROR] Something weird has happened - the same file is trying to be deleted"
    fi
    
done < "${1}"
