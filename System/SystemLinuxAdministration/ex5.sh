awk -F: '{print $1}' /etc/passwd | sort


:'
'awk -F:'  : sets the field separator in awk to a colon (:). It specifies that each line in the input file should be split into fields based on the colon delimiter. 
'{print $1}':  print the first field ($1) of each line.
'sort' : sort the output of awk 



'
