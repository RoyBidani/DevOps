#!/bin/bash

echo "Enter name of directory:"
read dir_name

path=$(find ~ -type d -name "$dir_name" -quit 2>/dev/null)

cd "$path"

ls "$path" | wc -l


