#!/bin/bash

log_messege="Script executed successfully"
log_file="/var/log/syslog"
date=$(date +"%Y-%m-%d %H:%M:%S")

# the command that I want to track his succssefull run
ls -l /home/parallels/roy.bidani/

if [ $? -eq 0 ]; then
	log_entry="$date $(hostname) ${0##*/}: $log_message"
	echo "$log_entry" >> "$log_file"
fi

: <<'COMMENT'
:'
the script command ls -l /home/user/documents/ is executed.. After executing the command, the script checks the exit status using $?. If the exit status is 0, indicating a successful execution of the command, it appends a log entry to the log file with the current date, hostname, script name, and the log message.

to run the program:
sudo bash ex4.sh

'
COMMENT

