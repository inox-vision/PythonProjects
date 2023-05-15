import os
import os.path
import shutil

# This script moves all files one folder up.

files_location = input("Paste path to folder where files are to be deleted:")
counter = 0

for dirpath, dirs, files in os.walk(files_location):
    for file in os.scandir(dirpath):
        if os.path.isfile(file):
            dir_to_move_h, dir_to_move_t = os.path.split(dirpath)
            file_to_move_h, file_to_move_t = os.path.split(file.path)
            final_file = os.path.join(dir_to_move_h, file_to_move_t)
           
            shutil.copy2(file.path, final_file)
            os.remove(file.path)
            counter = counter + 1
            
print(f"{counter} files were moved.")