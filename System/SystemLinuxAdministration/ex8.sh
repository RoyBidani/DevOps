find / -size +50M -exec ls -lh {} + 2>/dev/null | sort -k5


:'
-exec ls -lh {} +: This is an action performed on the files found by find.
searches the entire system ("/") for files larger than 50 MB, lists them using ls -lh to display human-readable file sizes, and then sorts the output based on the file size (ascending order).
The -lh options in ls display file sizes in a human-readable format and provide detailed information about each file.
sort -k5: This command takes the output of the previous ls command and sorts it based on the fifth column. In this case, the fifth column represents the file size. The -k5 option specifies that the sorting should be based on the fifth column.

'
