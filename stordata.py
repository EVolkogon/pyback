#!/usr/bin/python
"""
File with classes for backup script
"""
#used 
from os import system, stat, walk
from datetime import datetime
from subprocess import call

class Data ( object ):
    """Dont forget write the comments!!!!) """
    
    def __init__( self, path_to_data ):
        """ """
        self.path = path_to_data
        self.name = path_to_data.split('/')[-1]
        self.path_location = "/".join(path_to_data.split('/')[:-1])
        
    def get_name( self ):
        """ """
        return self.name
        
    def get_location( self ):
        
        return self.path_location
        
    def save_data( self, path_to_save):
        """ """
        save =  str("cd " + self.path_location 
                          + " && tar -czpf " 
                          + "/" + path_to_save + "/" + self.name + ".tar.gz"
                          + " " + self.name)
        res = system(save) # run execute and store result of command 
        if res == 0:
            return True
        else:
            return False
            
    def restore_data( self, path_to_save ):
        """ """
        restore = str("tar" + " -xzpf " 
                            + path_to_save + self.name + ".tar.gz"
                            + " -C " + self.path_location)
        res = system(restore) # run execute and store result of command 
        if res == 0:
            return True
        else:
            return False
        
    def __str__( self ):
        """ """
        return "File to save: " + self.name
        
    def __repr__( self ):
        """ """
        return "File to save: " + self.name
    def __eq__(self, other):
        return self.name == other.name
    def __hash__(self):
        return hash(self.name)
        
class Storage ( object ):
    """ """
    def __init__( self, path_to_storage ):
        """ """
        #base
        self.status = True 
        self.path = path_to_storage
        self.name = path_to_storage.split('/')[-1]
        # set now date as current work folder
        self.current_date = self.path # set folder for current actul backup
        if self._create_current_date_folder() != 0:
            self.status = False
    
    def get_status(self):
        return self.status

    #methods create
    def _create_folder( self, path_to_fold, fold_name ):
        """ This method create folder """
        new_folder = str("mkdir " + path_to_fold + "/" + fold_name)
        return (system(new_folder), path_to_fold + "/" + fold_name) # return a tuple where fistr is execute code (0 - is good!), second is new path
        
    def _create_current_date_folder( self ):
        """ """
        try:
            folds_ctimes = set([fold for fold in walk(self.path).next()[1]])
        except:
            return -1
        now = datetime.now()
        now_folder = "%s%s%s" % (now.year, now.month, now.day)
        if now_folder not in folds_ctimes:
            res = self._create_folder(self.path, now_folder)
            if res[0] == 0:
                self.current_date = res[1]
                return res[0]
            else:
                return res[0]
        else:
            self.current_date =self.path + "/"+"%s%s%s" % (now.year, now.month, now.day)
            return 0

    def _create_profile_folder ( self, profile ):
        
        #self._create_current_date_folder()     kostiling and velosepeding!!!!
        profile_fold_list = set([fold for fold in walk(self.current_date).next()[1]])
        if profile not in profile_fold_list:
            return self._create_folder(self.current_date, profile)
        else:
            return (0, self.current_date + "/" + profile)
            
    def save( self, profile, data_obj_list ):
        """ """
        res = self._create_profile_folder( profile )
        if res[0] != 0:
            return "error " + profile
        else:
            now = datetime.now()
            now_folder = "%s%s%s" % (now.hour, now.minute, now.second)
            work_folder = res[1]
            
            del res
            res = self._create_folder(work_folder, now_folder)
            if res[0] != 0:
                return "error " + now_folder
            else:
                status = []
                for data_obj in data_obj_list:
                    if not data_obj.save_data(res[1]):
                        status.append("error: " + data_obj.get_name())
                return status
    
    #methods get
    def get_date_folders( self ):
        """ """
        return [fold for fold in walk(self.path).next()[1]]
    
    def get_profile_folders( self ):
    
        return [fold for fold in walk(self.current_date).next()[1]]
        
    def get_time_folders( self, profile ):
    
        return [fold for fold in walk(self.current_date + "/" + profile).next()[1]]
    
    def get_backup_files( self, profile, time ):
    
        return [fold for fold in walk(self.current_date + "/" + profile + "/" + time).next()[2]]

    #methods set
    
    def set_current_date( self, date):
        
        if date in set([fold for fold in walk(self.path).next()[1]]):
            self.current_date = self.path + "/" + date
            return "Sucessfuly set folder:  " + date
        else:
            return "No folder with date: " + date
            
    #restore methods
    
    def restore ( self, date, profile , time, restore_list ) :
        """ """
        restore_path = self.path + "/" + date + "/" + profile + "/" + time + "/"
        status = []
        for data_obj in restore_list:
            if not data_obj.restore_data(restore_path):
                status.append("error: " + data_obj.get_name())
        return status
        
    def __str__( self ):
        """ """
        return self.name
        
    def __repr__( self ):
        """ """
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __hash__(self):
        return hash(self.name)
        
        
        
        
        
        
        