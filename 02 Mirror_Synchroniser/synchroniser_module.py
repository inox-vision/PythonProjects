import os
import shutil
import os.path
from time import strftime, localtime, time

class Synchroniser:

    source_files_list =[]
    source_dirs_list = []
    dest_files_list = []
    dest_dirs_list = []

    deleted_files = 0
    copied_files = 0
    backed_up_files = 0
    
    def __init__(self, source_dir, dest_dir, ignore_list, use_history, days_to_backup):

        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.ignore_list = ignore_list
        self.days_to_backup = days_to_backup
        self.use_history = use_history

        dest_dir_head, dest_dir_tail = os.path.split(self.dest_dir)
        self.history_dir = dest_dir_head+'/.'+dest_dir_tail+'_history'

        self.snapshot_time = strftime(f'%Y_%m_%d__%H_%M_%S', localtime())

        self.dest_dir_available = os.path.exists(dest_dir) and os.path.exists(source_dir)


class MirrorSynchroniser (Synchroniser):

    
    def make_history_dir(self):
                
        try:
            os.mkdir(self.history_dir)
        except:
            pass
        
        
    def create_source_lists (self):
        for dirpath, dirs,files in os.walk(self.source_dir):
            for source_files in os.scandir(dirpath):
                if not source_files.path.startswith(tuple(self.ignore_list)):
                    if source_files.is_file():
                        Synchroniser.source_files_list.append(os.path.relpath(source_files.path, self.source_dir))
                    if source_files.is_dir():
                        Synchroniser.source_dirs_list.append(os.path.relpath(source_files.path, self.source_dir))


    def create_destination_lists (self):
        for dirpath, dirs,files in os.walk(self.dest_dir):
            for dest_files in os.scandir(dirpath):
                if not dest_files.path.startswith(tuple(self.ignore_list)):
                    if dest_files.is_file():
                        Synchroniser.dest_files_list.append(os.path.relpath(dest_files.path, self.dest_dir))
                    if dest_files.is_dir():
                        Synchroniser.dest_dirs_list.append(os.path.relpath(dest_files.path, self.dest_dir))        
    
    
    def clean_history(self):
        for dirpath,dirs,files in os.walk(self.history_dir):
            for history_files in os.scandir(dirpath):
                if history_files.is_file():
                    actual_time = time()
                    creation_time = os.path.getctime(history_files.path)
                    time_difference = actual_time - creation_time
                    if time_difference > self.days_to_backup*24*60*60:
                        os.remove(history_files.path)
                        print(history_files.path, " deleted from history")
            for history_dirs in os.scandir(dirpath):
                if history_dirs.is_dir() and len(os.listdir(history_dirs.path)) == 0:
                    os.rmdir(history_dirs.path)


    def clean_destination(self):
        for dirpath, dirs, files in os.walk(self.dest_dir):
            for dest_files in os.scandir(dirpath):
                dest_file_path = os.path.relpath(dest_files.path, self.dest_dir) 
                if dest_files.is_file():
                    if dest_file_path not in Synchroniser.source_files_list:
                        subfolder = os.path.relpath(dirpath, self.dest_dir)               
                        if self.use_history:    
                            try:
                                os.makedirs(f"{self.history_dir}/{subfolder}")
                            except:
                                pass 
                            filename, extension = os.path.splitext(dest_files.name)
                            shutil.copy2(dest_files.path, f"{self.history_dir}/{subfolder}/{filename}_{self.snapshot_time}{extension}")
                            Synchroniser.backed_up_files += 1
                            print(os.path.relpath(dest_files.path, self.dest_dir), " moved to history")
                        print(os.path.relpath(dest_files.path, self.dest_dir), " deleted")
                        Synchroniser.deleted_files += 1
                        os.remove(dest_files.path)

        for dirpath, dirs, files in os.walk(self.dest_dir):
            for dest_folders in os.scandir(dirpath):
                if os.path.relpath(dest_folders.path, self.dest_dir) not in Synchroniser.source_dirs_list:
                    if dest_folders.is_dir():
                        shutil.rmtree(dest_folders.path)


    def create_folders(self):
        for dirpath, dir,files in os.walk(self.source_dir):
            for dirs in os.scandir(dirpath):
                if not dirs.path.startswith(tuple(self.ignore_list)):
                    if dirs.is_dir():
                        subfolder = os.path.relpath(dirs.path, self.source_dir)
                        try:
                            os.makedirs(f"{self.dest_dir}/{subfolder}")
                        except:
                            pass


    def copy_files (self):
        for dirpath,dirs,file in os.walk(self.source_dir):
            for files in os.scandir(dirpath):
                if not files.path.startswith(tuple(self.ignore_list)):
                    if files.is_file() and os.path.relpath(files.path, self.source_dir) not in Synchroniser.dest_files_list:
                        shutil.copy2(files.path, f"{self.dest_dir}/{os.path.relpath(dirpath, self.source_dir)}")
                        Synchroniser.copied_files += 1
                        print(os.path.relpath(files.path, self.source_dir)," copied")

        for dirpath, dirs, file in os.walk(self.dest_dir):
            for files in os.scandir(dirpath):
                if files.is_file():
                    
                    source_file_path = f"{self.source_dir}/{os.path.relpath(files.path, self.dest_dir)}"
                                            
                    src_file_modif_time = os.path.getmtime(source_file_path)
                    dest_file_modif_time = os.path.getmtime(files.path)
                    modif_time_difference = src_file_modif_time - dest_file_modif_time
                    
                    if modif_time_difference > 0:
                        subfolder = os.path.relpath(dirpath, self.dest_dir)
                        if self.use_history:
                            try:
                                os.makedirs(f"{self.history_dir}/{subfolder}")
                            except:
                                pass
                            
                            filename, extension = os.path.splitext(files.name)
                            shutil.copy2(files.path, f"{self.history_dir}/{subfolder}/{filename}_{self.snapshot_time}{extension}")
                        shutil.copy2(source_file_path, files.path)
                        Synchroniser.copied_files += 1
                        print(os.path.relpath(source_file_path, self.source_dir) , " copied")
                        

    def synchronise(self):

        if self.dest_dir_available:
            if self.use_history:
                self.make_history_dir()
            
            self.create_source_lists()
            self.create_destination_lists()
        
            if self.use_history:
                self.clean_history()
            
            self.clean_destination() 
            self.create_folders()    
            self.copy_files()

            total_operations = Synchroniser.backed_up_files + Synchroniser.copied_files + Synchroniser.deleted_files
            print(f"\nSynchronisation finished with {total_operations} operations.")
            print(f"{Synchroniser.backed_up_files} files has been backed up for {self.days_to_backup} days.")
            print(f"{Synchroniser.deleted_files} files has been deleted in destination folder.")
            print(f"{Synchroniser.copied_files} files has been copied to destination folder.")

        else:
            print("Check paths. Source/Destination directory or both are not available.\nProgram has nothing to do.")
