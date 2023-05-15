import os
import os.path

# This script searches for files with
# specified extension and deletes them.

files_location = input("Paste path to folder where files are to be deleted:")
files_extension = input("insert file extension (without '.')")
counter = 0

for dirpath, dirs, files in os.walk(files_location):
    for file in os.scandir(dirpath):
        if file.path.endswith(files_extension):
            try: 
                os.remove(file.path)
                counter = counter + 1
            except:
                print(f"could not delete {file.path}" )

print(f"{counter} files were deleted.")