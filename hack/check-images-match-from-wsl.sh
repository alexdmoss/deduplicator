#!/usr/bin/env bash
#
# Just a little hack script for me to feel a bit more confident that the python code
# has definitely matched identical photos correctly before I delete them forever.
#
# Randomly picks $samples_to_check files from input file then opens the two images
# from WSL (the machine with all the images on it) using its default image viewer.

samples_to_check=10
num_lines=$(wc -l "${1}" | awk '{print $1}')

while [[ $i -lt ${samples_to_check} ]]; do

    rand=$((1 + RANDOM % "${num_lines}"))

    line=$(sed "${rand}q;d" "${1}")
    file1=$(echo "${line}" | awk -F\| '{print $1}' | sed 's#/mnt/c/#c:/#')
    file2=$(echo "${line}" | awk -F\| '{print $3}' | sed 's#/mnt/c/#c:/#')

    wslview "${file1}" &
    sleep 1
    wslview "${file2}" &
    sleep 1

    i=$((i+1))

done
