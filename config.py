"""
This is module with configuration. Latter it be rewrite to JSON format.
Use absolute path ONLY!
"""
         #Config Name   Config Unit

# dynamic path for test ONLY!
import os
script_path = os.path.dirname(os.path.realpath(__file__))

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
print CONFIG["DATA"]["LONERS"][0]