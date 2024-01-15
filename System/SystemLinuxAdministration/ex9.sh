echo "Hello, world!" > original_file.txt
ln original_file.txt hardlink.txt


:'
any changes made to either "original_file.txt" or "hardlink.txt" will be reflected in both files since they point to the same underlying data.

'
