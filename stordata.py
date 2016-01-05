#!/usr/bin/python
"""
File with classes for backup script
"""
from os import system, walk
from datetime import datetime


class Data(object):
    """This class have information about path to data
     and methods to create and restore data from archive"""

    def __init__(self, path_to_data):
        """ """
        self.path = path_to_data
        self.name = path_to_data.split('/')[-1]
        self.path_location = "/".join(path_to_data.split('/')[:-1])

    def get_name(self):
        """Return name of data """

        return self.name

    def get_location(self):
        """Get location to data"""

        return self.path_location

    def save_data(self, path_to_save):
        """ This method take path to backup storage as argument,
            create archive with data and put archive to backup storage
        """
        save = str("cd " + self.path_location
                   + " && tar -czpf "
                   + "/" + path_to_save + "/" + self.name + ".tar.gz"
                   + " " + self.name)
        res = system(save)  # run execute and store result of command
        if res == 0:
            return True
        else:
            return False

    def restore_data(self, path_to_save):
        """This method take path to backup storage as argument,
            and restore data from archive to vanilla data path"""
        restore = str("tar" + " -xzpf "
                      + path_to_save + self.name + ".tar.gz"
                      + " -C " + self.path_location)
        res = system(restore)  # run execute and store result of command
        if res == 0:
            return True
        else:
            return False

    def __str__(self):
        """return data object in string """
        return "File to save: " + self.name

    def __repr__(self):

        return "File to save: " + self.name

    # for set
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Storage(object):
    """This class have information about backup storage,
        prepare backup folders and
        manipulate with Data objects"""

    def __init__(self, path_to_storage):
        """Take and save path to backup storage.
            If be any problem in prepare folder, status change to False.
            Init can delete old folder if current number of folder > self.lifenumber
        """
        parse_from_cfg = path_to_storage.split('*')
        # base
        self.status = True
        self.path = parse_from_cfg[0]
        self.name = self.path.split('/')[-1]
        # set now date as current work folder
        self.current_date = self.path  # set folder for current actual backup
        if self.__create_current_date_folder() != 0:
            self.status = False
        # set time to life in number of folders
        if len(parse_from_cfg) > 1:
            self.lifenumber = parse_from_cfg[1]
            self.__del_old_fold()
    def get_status(self):
        """Return status of backup storage"""
        return self.status

    # methods create
    @staticmethod
    def __create_folder(path_to_fold, fold_name):
        """ This method create folder """
        new_folder = str("mkdir " + path_to_fold + "/" + fold_name)
        return (system(new_folder),
                path_to_fold + "/" + fold_name)  # return a tuple where fistr is execute
                                                 # code (0 - is good!), second is new path

    def __create_current_date_folder(self):
        """This method create folder with current date. If be any problem in this method
         it return non zero value. If all ok self.current_date change to current date"""
        try:
            folds_ctimes = set([fold for fold in walk(self.path).next()[1]])
        except Exception:
            return -1
        now = datetime.now()
        now_folder = "%s-%s-%s" % (now.year, now.month, now.day)
        if now_folder not in folds_ctimes:
            res = self.__create_folder(self.path, now_folder)
            if res[0] == 0:
                self.current_date = res[1]
                return res[0]
            else:
                return res[0]
        else:
            self.current_date = self.path + "/" + "%s-%s-%s" % (now.year, now.month, now.day)
            return 0

    def __create_profile_folder(self, profile):
        """Take data profile and create folder with same name """
        profile_fold_list = set([fold for fold in walk(self.current_date).next()[1]])
        if profile not in profile_fold_list:
            return self.__create_folder(self.current_date, profile)
        else:
            return 0, self.current_date + "/" + profile

    def __del_old_fold(self):
        """
        Use self.lifetime parameter(in days) to delete old folders
        """
        if 0 < int(self.lifenumber) < len(self.get_date_folders()):
            sort_date_fold = sorted(self.get_date_folders(), reverse=True)
            if self.current_date.split('/')[-1] in sort_date_fold:
                del sort_date_fold[sort_date_fold.index(self.current_date.split('/')[-1])]
            print sort_date_fold
            list_for_delete = sort_date_fold[int(self.lifenumber):]
            for folder in list_for_delete:
                del_cmd = "rm -rf " + self.path + "/" + folder
                system(del_cmd)

    def save(self, profile, data_obj_list):
        """ Take data profile and list of Data objects.
         Use Data methods to create backups"""
        res = self.__create_profile_folder(profile)
        if res[0] != 0:
            return "error " + profile
        else:
            now = datetime.now()
            now_folder = "%s-%s-%s" % (now.hour, now.minute, now.second)
            work_folder = res[1]

            del res
            res = self.__create_folder(work_folder, now_folder)
            if res[0] != 0:
                return "error " + now_folder
            else:
                status = []
                for data_obj in data_obj_list:
                    if not data_obj.save_data(res[1]):
                        status.append("error: " + data_obj.get_name())
                return status

    # methods get
    def get_date_folders(self):
        """Return list of date folders from storage """
        return [fold for fold in walk(self.path).next()[1]]

    def get_profile_folders(self):
        """Return profile list from current date"""
        return [fold for fold in walk(self.current_date).next()[1]]

    def get_time_folders(self, profile):
        """Return time-folders from profile folder"""
        return [fold for fold in walk(self.current_date + "/" + profile).next()[1]]

    def get_backup_files(self, profile, time):
        """Return all data from time"""
        return [fold for fold in walk(self.current_date + "/" + profile + "/" + time).next()[2]]

    # methods set

    def set_current_date(self, date):
        """ Set current folder for work"""
        if date in set([fold for fold in walk(self.path).next()[1]]):
            self.current_date = self.path + "/" + date
            return "Successfully set folder:  " + date
        else:
            return "No folder with date: " + date

    def set_name(self, name):
        """Method for add not default storage name"""
        self.name = str(name)

    # restore methods

    def restore(self, date, profile, time, restore_list):
        """Get all information about path to archive with data
            and data list objects to restore.
            if restore end with errors, method return list with problem data"""
        restore_path = self.path + "/" + date + "/" + profile + "/" + time + "/"
        status = []
        for data_obj in restore_list:
            if not data_obj.restore_data(restore_path):
                status.append("error: " + data_obj.get_name())
        return status

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
