#! /usr/bin/python
"""
This module create(generate) json config file
"""
from os import path, stat
from json import load, dump

# dynamic path for test ONLY!
script_path = path.dirname(path.realpath(__file__))
config_path = path.join(script_path, "config.json")
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


def read_json(func):
    """
    Decorator function to read data from json file
    """
    if stat(config_path).st_size == 0:
        print "Config file is empty"

    def open_and_write(*data):
        with open(config_path) as json_data_file:
            config = load(json_data_file)
            return func(config, data)
    return open_and_write


def read_n_write_to_json(func):
    """
    decorator function to read and save data in json file
    """
    if stat(config_path).st_size == 0:
        print "Config file is empty"

    def reader_writer(*data):
        with open(config_path) as json_data_file:
            config = load(json_data_file)
        with open(config_path, 'w') as json_data_file:
            dump(func(config, data), json_data_file)
    return reader_writer


@read_n_write_to_json
def create_not_zero_json(config, data):
    config = {"STORAGES": {}, "DATA": {}}
    return config


@read_n_write_to_json
def set_default_config(config, data):
    config = DEF_CONFIG
    return config


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


@read_n_write_to_json
def add_profile(config, data):
    profile_name = data[0]
    config["DATA"][profile_name] = []
    return config


@read_n_write_to_json
def add_data_path(config, data):
    profile_name = data[0]
    data_path = data[1]

    if profile_name in config["DATA"].keys():
        if data_path in config["DATA"][profile_name]:
            print "path exist " + data_path
        else:
            config["DATA"][profile_name].append(data_path)
    else:
        print "No " + profile_name + " in config"

    return config


@read_n_write_to_json
def add_storage(config, data):

    storage_name = data[0]
    storage_path = data[1]

    if storage_name not in config["STORAGES"].keys():
        config["STORAGES"][storage_name] = storage_path

    return config


@read_n_write_to_json
def del_profile(config, data):

    profile_name = data[0]

    if profile_name in config["DATA"].keys():
        del config["DATA"][profile_name]
    else:
        print "No profile with name - " + profile_name

    return config


@read_n_write_to_json
def del_path(config, data):
    profile_name = data[0]
    data_path = data[1]

    if profile_name in config["DATA"].keys():
        if data_path in config["DATA"][profile_name]:
            del config["DATA"][profile_name][config["DATA"][profile_name].index(data_path)]
        else:
            print "No " + data_path + " in config"
    else:
        print "No " + profile_name + " in config"

    return config


@read_n_write_to_json
def del_storage(config, data):
    storage_name = data[0]

    if storage_name in config["STORAGES"].keys():
        del config["STORAGES"][storage_name]
    else:
        print "No " + storage_name + " in config"

    return config


@read_json
def get_profile_list(config, data):

    return config["DATA"].keys()


@read_json
def get_path_list(config, data):
    profile_name = data[0]

    return config["DATA"][profile_name]


@read_json
def get_storage_list(config, data):

    return config["STORAGES"].keys()
