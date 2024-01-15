#!/bin/bash

log_messege="Script executed successfully"
log_file="/var/log/syslog"
date=$(date +"%Y-%m-%d %H:%M:%S")

# the command that I want to track his succssefull run
ls -l /home/parallels/roy.bidani/

# Intentional syntax errors
undefined_command
echo "This line will not be executed"


if [ $? -eq 0 ]; then
	log_entry="$date $(hostname) ${0##*/}: $log_message"
	echo "$log_entry" >> "$log_file"
fi

: <<'COMMENT'

:'
runing the script with strace and redirect the output to a file:

strace -o strace_output.txt bash ex5.sh

This command executes the script and traces the system calls, saving the output to strace_output.txt.

then we find the error:
grep "error" strace_output.txt


at the strace_output.txt file we can find the exact time of the error by checking the properties and the modified time.
'
COMMENT
