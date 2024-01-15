#!/bin/bash

sudo netstat -tlnp | awk 'NR>2 {split($NF,a,"/"); printf "%-20s %s\n", a[2], $4}'

chmod +x activesockets.sh 	

sudo mv activesockets /usr/local/bin	// made it accessible to all users in the system by placing it in a directory included in the systems PATH environment variable.




: '
expalin :
-- 'netstat -tlnp' : display active network connections and listening sockets. 

-t: Shows TCP connections.
-l: Displays listening sockets.
-n: Displays IP addresses and port numbers instead of resolving them to hostnames and services.
-p: Shows the PID and name of the program using the socket.


-- " awk 'NR>2 {split($NF,a,"/"); printf "%-20s %s\n", a[2], $4} " : print both the program name or process ID (extracted from the last field) and the listening socket (extracted from the fourth field). The printf statement formats the output by using a width of 20 characters for the program name or process ID (%-20s) and printing the socket address ($4).


' NR>2 ': Specifies a condition that only lines with a record number greater than 2 should be processed. This skips the first two lines of the netstat output, which are headers.

split($NF,a,"/"): This split function splits the last field ($NF) of each input line into an array a, using the delimiter /. The NF variable in awk represents the total number of fields in the current input line, and $NF refers to the value of the last field.

printf "%-20s %s\n", a[2], $4: This printf statement formats and prints the output. It consists of two placeholders (%s) separated by a space. The first placeholder %s is replaced with the value of a[2], which corresponds to the program name or process ID extracted from the last field. The second placeholder %s is replaced with the value of $4, which represents the fourth field containing the listening socket. The -20s specifies a left-aligned width of 20 characters for the program name or process ID.'

the output:
systemd-resolve      127.0.0.53:53
cupsd                127.0.0.1:631
usr                  0.0.0.0:22
cupsd                ::1:631
usr                  :::22

It lists the programs or process IDs that own the listening sockets along with the corresponding socket addresses. 
'

