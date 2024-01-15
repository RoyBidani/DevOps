#!/bin/bash

echo "Enter a directory path:"
read usr_path

ls $usr_path | wc -l
