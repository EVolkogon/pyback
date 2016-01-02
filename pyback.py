#! /usr/bin/python
from stordata import Data, Storage 
from config import CONFIG
from sys import argv, exit
from getopt import getopt, GetoptError
from os import path
import logging

# start initialization logging. Take from https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
script_path = path.dirname(path.realpath(__file__))
logger = logging.getLogger(' ')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(script_path+'/log.txt')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
# end logging initialization
def main(argv):
    profile_list = []
    storage_list = []
    try:
        opts, args = getopt(argv,"mhd:s:",["data=","storages"])
    except GetoptError:
        print "Incorrect key. \nExample: pyback -d PROFILE1,PROFILE2 -s STORAGE1,STORAGE2\n Or try key '-h' for help"
        exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "\nExample: pyback -d PROFILE1,PROFILE2 -s STORAGE1,STORAGE2"
            print "-m for menu"
            exit()
        elif opt == "-m":
            from textMenu import menu
            menu()
        elif opt in ('-d', 'data'):
            for item in arg.split(','):
                profile_list.append(item)
        elif opt in ('-s', 'storages'):
            for item in arg.split(','):
                storage_list.append(item)

    if profile_list and storage_list:
        logger.info('BackUp start')
        if set(storage_list) == set(CONFIG["STORAGES"].keys()):
            storage_obj_list = []
            for storage in storage_list:
                storage_obj = Storage(CONFIG["STORAGES"][storage])
                storage_obj.set_name(storage)
                storage_obj_list.append(storage_obj)
            # check store status and write to log
            for obj in storage_obj_list:
                if obj.get_status():
                    logger.info(obj.name + " Ok!")
                else:
                    logger.error(obj.name + " Check it!!!")
            for profile in profile_list:
                data_obj_list = [Data(data) for data in CONFIG["DATA"][profile]]
                for storage in storage_obj_list:
                    status = storage.save(profile, data_obj_list)
                    # if for log
                    if status:
                        logger.error("Problem to save data from profile - " + profile)
                        for data_error in status:
                            logger.error(data_error)
                    else:
                        logger.info(storage.name + " " + profile + " successfully save")
        else:
            print "Check profile and storage list!"
            logger.warn('BackUp stop')


main(argv[1:])