#! /usr/bin/python
"""
This module create(generate) json config file
"""
from os import path
from json import load, dump
# dynamic path for test ONLY!
script_path = path.dirname(path.realpath(__file__))

# default test config
CONFIG = {  "DATA":     # Profile
                        { "LONERS": #Path
                                    [script_path + "/test/DATA/save_me.txt",
                                     script_path +"/test/DATA/folder_for_save",
                                      ],
                         "Project" : ["./"],
                        },
            "STORAGES":
                        {"STOR_1" :script_path +"/test/DIR_FOR_BKP",
                         },
         }

with open(script_path + '/config.json', 'wb') as json_data_file:
    dump(CONFIG, json_data_file)
    json_data_file.close()
