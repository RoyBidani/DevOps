#!/bin/bash

echo "Enter name of directory:"
read dir_name
echo "Enter max size"
read max

path=$(find ~ -type d -name "$dir_name" -quit 2>/dev/null)


find "$path" -type f -size +"max" c -exec rm {} 


