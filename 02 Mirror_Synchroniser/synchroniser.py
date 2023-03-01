from synchroniser_module import MirrorSynchroniser


synchro_list = {
    'source_dir' : '<source_dir_here>',
    'dest_dir' : '<destination_dir_here>',
    'ignore_list' : [],
    'use_history' : True,
    'days_to_backup' : 14,
}
   
synchroniser = MirrorSynchroniser(**synchro_list)

synchroniser.synchronise()