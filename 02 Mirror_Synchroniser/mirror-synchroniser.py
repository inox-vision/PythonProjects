from synchroniser import MirrorSynchroniser


source_dir = '/home/adrian/Insync/blindesign.pl@gmail.com/OneDrive/PROGRAMOWANIE/Python/UNDER DEVELOPMENT/Synchroniser/synchro_A'
dest_dir = '/home/adrian/Insync/blindesign.pl@gmail.com/OneDrive/PROGRAMOWANIE/Python/UNDER DEVELOPMENT/Synchroniser/synchro_B'
ignore_list = []
use_history = True
days_to_backup = 14

   
synchroniser = MirrorSynchroniser(source_dir, dest_dir, ignore_list, use_history, days_to_backup)


synchroniser.synchronise()