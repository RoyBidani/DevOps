a.
touch myfile.txt
ls -l myfile.txt		// check default premissions

output:
"-rw-rw-r--"
read and write permissions for both the owner and group, and read-only 		                permissions for others.
there is no exceute premissions by deafult on newly created files even if you set mask to have those premissions (except dir)

chmod u+rw myfile.txt		//read and write premissions for the user
chmod o+x myfile.txt		//execute premission for others 
or
chmod 600 myfile.txt		//read and write premissions for the owner and no presmissions for the group and others
chmod 701 myfile.txt		//read and write, premissions for the owner and the group has no permissions, and others have execute permissions.

b. 
the umask value determines which permission bits are turned off when creating new files.
to set a default umask value of '027' where the group and others have no permissions:
umask 027


