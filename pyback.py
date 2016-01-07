#! /usr/bin/python
"""
SYNOPSIS

    pyback [-d] data_profile [-s] storage ['--set_default', '--set_base',
                                                 '--add_profile', '--add_path', '--add_storage',
                                                 '--del_profile', '--del_path', '--del_storage']

DESCRIPTION

    This script create file and folder backup in your safe storage(s).
    Also it help you to create configuration for your backups.

    It very easy to use: consolidate your data in 'profile(s)', add your storages
    and save what/where/when you want in one short command(Cron) line.
    See more in examples

EXAMPLES

    For example we create apache2 backup in 4 steps.

    0) If it's your first script run, you must create basic config.
        all you need just run script with key ''--set_base':
                pyback.py --set_base

    1) Add profile "APACH":
                pyback.py --add_profile APACH

    2) Add data path(s) to Profile:
                pyback.py --add_path APACH:/etc/apache2/apache2.conf,/etc/apache2/sites-enabled,/mnt/www/sites

    3) Add name and path to safe folder:
                pyback.py --add_storage STOR_1:/mnt/backup_folder/
    4) Now you ready to backup your data:
                pyback.py -d APACH -s STOR_1


    Before you start save your data, practice on test folder. For it just load default config:
                pyback.py --set_default


AUTHOR

    E.Volkogon: e.volgon@gmail.com
    github:     https://github.com/EVolkogon
"""
from stordata import Data, Storage
from sys import argv, exit
from getopt import getopt, GetoptError
from os import path
from json import load
from logging import Formatter, FileHandler, getLogger, DEBUG
import config

script_path = path.dirname(path.realpath(__file__))  # set current script folder

# initializing logging. Take from https://docs.python.org/2/howto/logging-cookbook.html#logging-cookbook
logger = getLogger(' ')
logger.setLevel(DEBUG)
fh = FileHandler(script_path + '/log.txt')
formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
# end initializing

# import config from json


def main(argument):
    global opts
    profile_list = []
    storage_list = []
    try:
        opts, args = getopt(argument, "mhd:s:", ['set_default', 'set_base',
                                                 'add_profile=', 'add_path=', 'add_storage=',
                                                 'del_profile=', 'del_path=', 'del_storage='])
    except GetoptError:
        print "Incorrect key. \nExample: pyback -d PROFILE1,PROFILE2 -s STORAGE1,STORAGE2\n Or try key '-h' for help"
        exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print __doc__
            exit()
        elif opt == "-m":
            from textMenu import menu
            menu(CONFIG, Data, Storage)

        elif opt == '-d':
            for item in arg.split(','):
                profile_list.append(item)

        elif opt == '-s':
            for item in arg.split(','):
                storage_list.append(item)

        elif opt == '--set_default':
            print "Config set to default"
            config.set_default_config()

        elif opt == '--set_base':
            config.set_base()

        elif opt == '--add_storage':
            for pair in arg.split(','):
                name, s_path = pair.split(':')
                config.add_storage(name, s_path)

        elif opt == '--add_profile':
            config.add_profile(str(arg))

        elif opt == '--add_path':
            profile, paths = arg.split(':')
            for data_path in paths.split(','):
                config.add_data_path(profile, data_path)
        elif opt == '--del_profile':
            config.del_profile(arg)

        elif opt == '--del_path':
            profile, paths = arg.split(':')
            for data_path in paths.split(','):
                config.del_path(profile, data_path)

        elif opt == '--del_storage':
            config.del_storage(arg)

    if profile_list and storage_list:
        logger.info('BackUp start')
        if set(storage_list) == set(CONFIG["STORAGES"].keys()):
            storage_obj_list = []
            for storage in storage_list:
                storage_obj = Storage(CONFIG["STORAGES"][storage])
                storage_obj.set_name(storage)
                storage_obj_list.append(storage_obj)
            # check storage status and write to log
            for obj in storage_obj_list:
                if obj.get_status():
                    logger.info(obj.name + " Ok!")
                else:
                    logger.error(obj.name + " Check it!!!")

            for profile in profile_list:
                if profile in config.get_profile_list():
                    data_obj_list = [Data(data) for data in CONFIG["DATA"][profile]]
                    for storage in storage_obj_list:
                        if str(storage) in config.get_storage_list():
                            status = storage.save(profile, data_obj_list)
                            # if for log
                            if status:
                                logger.error("Problem to save data from profile - " + profile)
                                for data_error in status:
                                    logger.error(data_error)
                            else:
                                logger.info(storage.name + " " + profile + " successfully save")
                        else:
                            print "No " + storage + " in config"
                else:
                    print "No " + profile + " in config"
        else:
            print "Check profile and storage list!"
            logger.warn('BackUp stop')

# need rewrite (in next open task) to another non zero file check.
with open(script_path + '/config.json') as json_data_file:
    try:
        CONFIG = load(json_data_file)
        main(argv[1:])

    except ValueError:
        if len(argv) > 1:
            if 'set' not in argv[1]:
                CONFIG = {}
                print "Check config.\n Try run with --set default or --set base\n Or -h for help"
            else:
                main(argv[1:])
