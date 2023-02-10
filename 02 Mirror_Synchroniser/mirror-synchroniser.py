import os, shutil, time, os.path


source_dir = '/home/adrian/Insync/blindesign.pl@gmail.com/OneDrive/PROGRAMOWANIE/Python/UNDER DEVELOPMENT/Synchroniser/synchro_A'
dest_dir = '/home/adrian/Insync/blindesign.pl@gmail.com/OneDrive/PROGRAMOWANIE/Python/UNDER DEVELOPMENT/Synchroniser/synchro_B'
use_history = False


dest_dir_head, dest_dir_tail = os.path.split(dest_dir)
history_dir = dest_dir_head+'/.'+dest_dir_tail+'_history'

days_to_backup = 14
dest_dir_available = os.path.exists(dest_dir)


# CREATING History directory

if dest_dir_available and use_history:
    try:
        os.mkdir(history_dir)
    except:
        pass

snapshot_time = time.strftime(f'%Y_%m_%d__%H_%M_%S', time.localtime())

source_list =[]
source_dirs_list = []
dest_list = []
dest_dirs_list = []

# Creating lists of files

def create_lists (directory,files_list, dirs_list):
    for dirpath, dirs,files in os.walk(directory):
        for source_files in os.scandir(dirpath):
            if source_files.is_file():
                files_list.append(os.path.relpath(source_files.path, directory))
            if source_files.is_dir():
                dirs_list.append(os.path.relpath(source_files.path, directory))

create_lists(source_dir, source_list, source_dirs_list)
create_lists(dest_dir, dest_list, dest_dirs_list)


# DELETE OLD files/folder in history

if use_history:
    for dirpath,dirs,files in os.walk(history_dir):
        for history_files in os.scandir(dirpath):
            if history_files.is_file():
                actual_time = time.time()
                creation_time = os.path.getctime(history_files.path)
                time_difference = actual_time - creation_time
                if time_difference > days_to_backup*24*60*60:
                    os.remove(history_files.path)
                    print(history_files.path, " deleted from history")
        for history_dirs in os.scandir(dirpath):
            if history_dirs.is_dir() and len(os.listdir(history_dirs.path)) == 0:
                os.rmdir(history_dirs.path)


# Backup deleted file and remove it from Destination folder  

if dest_dir_available:
    for dirpath, dirs, files in os.walk(dest_dir):
        for dest_files in os.scandir(dirpath):
            dest_file_path = os.path.relpath(dest_files.path, dest_dir) 
            if dest_files.is_file():
                if dest_file_path not in source_list:
                    subfolder = os.path.relpath(dirpath, dest_dir)               
                    if use_history:    
                        try:
                            os.makedirs(f"{history_dir}/{subfolder}")
                        except:
                            pass 
                        filename, extension = os.path.splitext(dest_files.name)
                        shutil.copy2(dest_files.path, f"{history_dir}/{subfolder}/{filename}_{snapshot_time}{extension}")
                        print(os.path.relpath(dest_files.path, dest_dir), " moved to history and deleted")
                    os.remove(dest_files.path)
    
# Delete directories which don't exist in source

for dirpath, dirs, files in os.walk(dest_dir):
    for dest_folders in os.scandir(dirpath):
        if os.path.relpath(dest_folders.path, dest_dir) not in source_dirs_list:
            if dest_folders.is_dir():
                shutil.rmtree(dest_folders.path)


# CREATE FOLDERS

if dest_dir_available:
    for dirpath, dirs,files in os.walk(source_dir):
        for dirs in os.scandir(dirpath):
            if dirs.is_dir():
                subfolder = os.path.relpath(dirs.path, source_dir)
                try:
                    os.makedirs(f"{dest_dir}/{subfolder}")
                except:
                    pass

# COPY NEW FILES

if dest_dir_available:
    for dirpath,dirs,files in os.walk(source_dir):
        for files in os.scandir(dirpath):
            if files.is_file() and os.path.relpath(files.path, source_dir) not in dest_list:
                shutil.copy2(files.path, f"{dest_dir}/{os.path.relpath(dirpath, source_dir)}")
                print(os.path.relpath(files.path, source_dir)," copied")


# COPY FILES IF CHANGED, keep version in History folder

if dest_dir_available:
    for dirpath, dirs, files in os.walk(dest_dir):
        for files in os.scandir(dirpath):
            if files.is_file():
                
                source_file_path = f"{source_dir}/{os.path.relpath(files.path, dest_dir)}"
                                        
                src_file_modif_time = os.path.getmtime(source_file_path)
                dest_file_modif_time = os.path.getmtime(files.path)
                modif_time_difference = src_file_modif_time - dest_file_modif_time
                
                if modif_time_difference != 0:
                    subfolder = os.path.relpath(dirpath, dest_dir)
                    if use_history:
                        try:
                            os.makedirs(f"{history_dir}/{subfolder}")
                        except:
                            pass
                        
                        filename, extension = os.path.splitext(files.name)
                        shutil.copy2(files.path, f"{history_dir}/{subfolder}/{filename}_{snapshot_time}{extension}")
                    shutil.copy2(source_file_path, files.path)
                    print(os.path.relpath(source_file_path, source_dir) , " copied")






