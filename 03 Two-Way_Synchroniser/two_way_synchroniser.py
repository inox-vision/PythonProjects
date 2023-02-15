import os, shutil, os.path
from time import strftime, localtime, time
from sys import exit

# czy A oraz B jest dostępne
# dodać math (floor)
# lista plikow/folderow
# ignore lista
# jeśli lista z pliku zewn jest pusta 


dir_A = '/home/adrian/Insync/blindesign.pl@gmail.com/OneDrive/PROGRAMOWANIE/Python/UNDER DEVELOPMENT/Synchroniser/synchro_A'
dir_B = '/home/adrian/Insync/blindesign.pl@gmail.com/OneDrive/PROGRAMOWANIE/Python/UNDER DEVELOPMENT/Synchroniser/synchro_B'
days_to_backup = 14

dir_A_head, dir_A_tail = os.path.split(dir_A)
dir_B_head, dir_B_tail = os.path.split(dir_B)
history_dir_A = dir_A_head+'/.'+dir_A_tail+'_history'
history_dir_B = dir_B_head+'/.'+dir_B_tail+'_history'

old_list_A_location = f"{dir_A}_old_list.txt"
old_list_B_location = f"{dir_B}_old_list.txt"

dirs_are_available = os.path.exists(dir_A) and os.path.exists(dir_B)

if not dirs_are_available:
    print("Check paths. One or both directories arenot available.\nProgram will terminate")
    exit()


# CREATING History directories
# try:
#     os.mkdir(history_dir_A)
# except:
#     pass

# try:
#     os.mkdir(history_dir_B)
# except:
#     pass

snapshot_time = strftime(f'%Y_%m_%d__%H_%M_%S', localtime())

dir_A_files_list =[]
dir_A_dirs_list = []
dir_B_files_list =[]
dir_B_dirs_list = []

old_list_A = []
old_list_B = []


# Read last directories state
try:
    with open(old_list_A_location, 'r') as file:
        old_list_A = file.read()
    with open(old_list_B_location, 'r') as file:
        old_list_B = file.read()
except:
    pass
    

# Creating current list of files
def create_lists ( directory, files_list, dirs_list):
    for dirpath, dirs,files in os.walk(directory):
        for source_files in os.scandir(dirpath):
            if source_files.is_file():
                files_list.append(os.path.relpath(source_files.path, directory))
            if source_files.is_dir():
                dirs_list.append(os.path.relpath(source_files.path, directory))

create_lists(dir_A, dir_A_files_list, dir_A_dirs_list)
create_lists(dir_B, dir_B_files_list, dir_B_dirs_list)


# DELETE OLD files/folder in history not yet implementd
def clear_history (directory):
    for dirpath,dirs,files in os.walk(directory):
        for history_files in os.scandir(dirpath):
            if history_files.is_file():
                actual_time = time()
                creation_time = os.path.getctime(history_files.path)
                time_difference = actual_time - creation_time
                if time_difference > days_to_backup*24*60*60:
                    os.remove(history_files.path)
                    print(history_files.path, " deleted from history")
        for history_dirs in os.scandir(dirpath):
            if history_dirs.is_dir() and len(os.listdir(history_dirs.path)) == 0:
                os.rmdir(history_dirs.path)

# clear_history(history_dir_A)
# clear_history(history_dir_B)



# Remove deleted file from Destination folder  
def delete_files (directory,files_list, old_list):
    for dirpath, dirs, files in os.walk(directory):
        for dest_files in os.scandir(dirpath):
            dest_file_path = os.path.relpath(dest_files.path, directory) 
            if dest_files.is_file() and dest_file_path not in files_list and dest_file_path in old_list:
                print(os.path.relpath(dest_files.path, directory), " deleted")
                os.remove(dest_files.path)



delete_files(dir_B, dir_A_files_list, old_list_B)
delete_files(dir_A, dir_B_files_list, old_list_A)


# Delete directories which don't exist in source

def delete_directories (directory):
    for dirpath, dirs, files in os.walk(directory):
        for dest_folders in os.scandir(dirpath):
            if dest_folders.is_dir():
                for dirpath2, dirs2, files2 in os.walk(dest_folders.path):
                    if len(files2) == 0:
                        shutil.rmtree(dest_folders.path)

delete_directories (dir_A)
delete_directories (dir_B)

create_lists(dir_A, dir_A_files_list, dir_A_dirs_list)
create_lists(dir_B, dir_B_files_list, dir_B_dirs_list)


# CREATE FOLDERS

def create_directories (source_dir, dest_dir):
    for dirpath, dirs,files in os.walk(source_dir):
        for dirs in os.scandir(dirpath):
            if dirs.is_dir():
                subfolder = os.path.relpath(dirs.path, source_dir)
                try:
                    os.makedirs(f"{dest_dir}/{subfolder}")
                except:
                    pass


create_directories (dir_A, dir_B)
create_directories (dir_B, dir_A)


# COPY NEW FILES

def copy_new_files (source_dir, dest_dir, dest_list):
    for dirpath,dirs,files in os.walk(source_dir):
        for files in os.scandir(dirpath):
            if files.is_file() and os.path.relpath(files.path, source_dir) not in dest_list:
                shutil.copy2(files.path, f"{dest_dir}/{os.path.relpath(dirpath, source_dir)}")
                print(os.path.relpath(files.path, source_dir)," copied")


copy_new_files(dir_A, dir_B, dir_B_files_list)
copy_new_files(dir_B, dir_A, dir_A_files_list)


# COPY FILES IF CHANGED

def copy_modified_files (dest_dir, source_dir):
    for dirpath, dirs, files in os.walk(dest_dir):
        for file in os.scandir(dirpath):
            if file.is_file():
                
                source_file_path = f"{source_dir}/{os.path.relpath(file.path, dest_dir)}"
                                        
                src_file_modif_time = os.path.getmtime(source_file_path)
                dest_file_modif_time = os.path.getmtime(file.path)
                modif_time_difference = src_file_modif_time - dest_file_modif_time
                
                if modif_time_difference > 0:
                    os.remove(file.path)
                    shutil.copy2(source_file_path, file.path)
                    print(os.path.relpath(source_file_path, source_dir) , " copied")

copy_modified_files(dir_B, dir_A)
copy_modified_files(dir_A, dir_B)


# Preparing current state for future synchronisation

dir_A_files_list.clear()
dir_B_files_list.clear()

create_lists(dir_A, dir_A_files_list, dir_A_dirs_list)
create_lists(dir_B, dir_B_files_list, dir_B_dirs_list)

with open(old_list_A_location, 'w') as file:
    file.write(str(dir_A_files_list))

with open(old_list_B_location, 'w') as file:
    file.write(str(dir_B_files_list))



