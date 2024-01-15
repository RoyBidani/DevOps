strace -e trace=write uname -a

:'
The strace command will trace the 'write' system calls made by the 'uname -a' command.
The 'write' system call in the output shows the string being written to the terminal

the write system call is used to write the string :
"Linux ubuntu-linux-22-04-desktop 5.15.0-72-generic #79-Ubuntu SMP Tue Apr 18 16:53:43 UTC 2023 aarch64 aarch64 aarch64 GNU/Linux" 
with a length of 129 bytes to the file descriptor 1, which represents standard output (the terminal).
'
