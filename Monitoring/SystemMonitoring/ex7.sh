:'
runing the command:
'
for i in 1 2 3 4; do while : ; do : ; done & done
:'
the output is processes ID:
'
[1] 187721
[2] 187722
[3] 187723
[4] 187724
:'
a. In the nmon terminal, we see an increase in CPU usage due to the busy loop created by the command.
b. To fix it, we can terminate the processes created by the command using the kill with the PIDs 
'
kill 187721 187722 187723 187724 

