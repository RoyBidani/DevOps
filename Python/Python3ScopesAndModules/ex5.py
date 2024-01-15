import os
import stat
import sys


def check_permissions(filename):
    # check if the name is file
    if os.path.isfile(filename):
        # os.stat(filename) returns file-related information, including the file mode (permissions).
        # os.stat(filename).st_mode extracts the file mode from the stat object.
        # stat.S_IMODE() takes the file mode as an argument and extracts the permissions
        permissions = stat.S_IMODE(os.stat(filename).st_mode)  # gets the file permissions as int

        # stat.S_IXUSR represents the executable permission for the owner
        # permissions & stat.S_IXUSR checks if the executable permission for the owner is set in the file permissions.
        is_executable = bool(permissions & stat.S_IXUSR)

        # Print the current permissions in octal format
        print(f"Current permissions for {filename}: {oct(permissions)}")

        # Check if executable permission for owner is not set
        if not is_executable:
            # Add executable permission for owner and group
            new_permissions = permissions | stat.S_IXUSR | stat.S_IXGRP

            # Change the permissions of the file to the new_permissions value
            os.chmod(filename, new_permissions)

            print(f"Changed permissions for {filename} to allow execution for owner and group.")
            print(f"Now current permissions for {filename}: {oct(new_permissions)}")

    else:
        print(f"File {filename} not found.")


# Get the file name from command line arguments
if len(sys.argv) > 1:
    filename = sys.argv[1]
    check_permissions(filename)
else:
    print("No file provided as a command line argument")