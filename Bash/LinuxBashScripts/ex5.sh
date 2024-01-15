#!/bin/bash

echo "Enter name of directory:"
read dir_name

path=$(find ~ -type d -name "$dir_name" -quit 2>/dev/null)

cd "$path"

for file in *; do
    if [ -f "$file" ]; then
        echo "$file: $(file -b "$file")"
    elif [ -d "$file" ]; then
        echo "$file: directory"
    fi
done
