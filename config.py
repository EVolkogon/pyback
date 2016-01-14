#! /usr/bin/python
"""
This module create(generate) json config file
"""
from os import path, stat
from json import load, dump

# dynamic path for test ONLY!
script_path = path.dirname(path.realpath(__file__))
config_path = script_path + "/config.json"
# default test config
DEF_CONFIG = {"DATA":  # Profile
                  {'LONERS':  # Path
                       [script_path + "/test/DATA/save_me.txt",
                        script_path + "/test/DATA/folder_for_save",
                        ],
                   },
              "STORAGES":
                  {"STOR_1": script_path + "/test/DIR_FOR_BKP",
                   },
              }


def create_not_zero_json():
    base = {"STORAGES": {}, "DATA": {}}
    with open(config_path, 'w') as json_data_file:
        dump(base, json_data_file)


def set_default_config():
    with open(config_path, 'w') as json_data_file:
        dump(DEF_CONFIG, json_data_file)


def set_base():
    # create config with empty values
    run = True
    while run:
        answer = raw_input("Are you sure?!(Y/n)")
        if answer.upper() == 'Y':
            create_not_zero_json()
            break
        elif answer.upper() == 'N':
            break
        else:
            print "Please repeat your answer. Only Y or N"


def add_profile(profile_name):
    if stat(config_path).st_size == 0:
        print "Config file is empty"
    with open(config_path) as json_data_file:
        config = load(json_data_file)
        if profile_name not in config["DATA"].keys():
            config["DATA"][profile_name] = []
    with open(config_path, 'w') as json_data_file:
        dump(config, json_data_file)


def add_data_path(profile_name, data_path):
    if stat(config_path).st_size == 0:
        print "Config file is empty"
    with open(config_path) as json_data_file:
        config = load(json_data_file)
        if profile_name in config["DATA"].keys():
            if data_path in config["DATA"][profile_name]:
                print "path exist " + data_path
            else:
                config["DATA"][profile_name].append(data_path)
        else:
            print "No " + profile_name + " in config"
    with open(config_path, 'w') as json_data_file:
        dump(config, json_data_file)


def add_storage(storage_name, storage_path):
    if stat(config_path).st_size == 0:
        print "Config file is empty"
    with open(config_path) as json_data_file:
        config = load(json_data_file)
        if storage_name not in config["STORAGES"].keys():
            config["STORAGES"][storage_name] = storage_path
    with open(config_path, 'w') as json_data_file:
        dump(config, json_data_file)


def del_profile(profile_name):
    if stat(config_path).st_size == 0:
        create_not_zero_json()
    with open(config_path) as json_data_file:
        config = load(json_data_file)
        if profile_name in config["DATA"].keys():
            del config["DATA"][profile_name]
        else:
            print "No profile with name - " + profile_name
    with open(config_path, 'w') as json_data_file:
        dump(config, json_data_file)


def del_path(profile_name, data_path):
    with open(config_path) as json_data_file:
        config = load(json_data_file)
        if profile_name in config["DATA"].keys():
            if data_path in config["DATA"][profile_name]:
                del config["DATA"][profile_name][config["DATA"][profile_name].index(data_path)]
            else:
                print "No " + data_path + " in config"
        else:
            print "No " + profile_name + " in config"
    with open(config_path, 'w') as json_data_file:
        dump(config, json_data_file)


def del_storage(storage_name):
    with open(config_path) as json_data_file:
        config = load(json_data_file)
        if storage_name in config["STORAGES"].keys():
            del config["STORAGES"][storage_name]
        else:
            print "No " + storage_name + " in config"
    with open(config_path, 'w') as json_data_file:
        dump(config, json_data_file)


def get_profile_list():
    if stat(config_path).st_size == 0:
        print "Config file is empty"
    with open(config_path) as json_data_file:
        config = load(json_data_file)
        return config["DATA"].keys()


def get_path_list(profile_name):
    if stat(config_path).st_size == 0:
        print "Config file is empty"
    with open(config_path) as json_data_file:
        config = load(json_data_file)
        return config["DATA"][profile_name]


def get_storage_list():
    if stat(config_path).st_size == 0:
        print "Config file is empty"
    with open(config_path) as json_data_file:
        config = load(json_data_file)
        return config["STORAGES"].keys()