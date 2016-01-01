from config import CONFIG
from stordata import Data, Storage
def menu():
    """
    This version of menu just for test/dev period.
    Must be rewritten because it's ugly
    """
    def printf(text):

        print text
    menu_run = True

    while menu_run:
        print "Choice menu item \n"
        print "%s\n%s\n%s" %  ("(C)rete backup", "(R)estore", "(Q)uit")
        print "-" * 16
        choice = raw_input("Enter your choice: ")
        # quit branch
        if choice.upper() == 'Q':
            menu_run = False
        #menu branch for create backup
        elif choice.upper() == 'C':
            sub_menu = True
            choice_set = set()
            storage_set = set()
            while sub_menu:
                print "#" *60
                num = 1
                for storage in sorted(CONFIG["STORAGES"].keys()):
                    print str(num) + ". " + storage + " Location: " + CONFIG["STORAGES"][storage],
                    if num in choice_set:
                        print "+"
                        new_store = Storage(CONFIG["STORAGES"][storage])
                        if new_store.get_status():
                            storage_set.add(new_store)
                        else:
                            print storage + ": " + "\nBad storage. Check it!" * 3
                    else:
                        print ""
                    num += 1
                print "\n"
                print "0." + " Select all storages\n", "(O)k\n", "(Q)uit\n", "(E)xit\n"
                print "-" * 16
                choice =  raw_input ("Choise storage(s): ")
                print "<"
                if choice.upper() == 'Q':
                    sub_menu = False
                elif not choice.isalpha() and int(choice) > 0 and int(choice) < num:
                    choice_set.add(int(choice))

                elif choice == '0':
                    sub_num = 1
                    for storage in CONFIG["STORAGES"].keys():
                        new_store = Storage(CONFIG["STORAGES"][storage])
                        if new_store.get_status():
                            storage_set.add(new_store)
                            choice_set.add(sub_num)
                            sub_num += 1
                        else:
                            print storage + ": " + "\nBad storage. Check it!" * 3

                elif str(choice).upper() == 'E':
                    menu_run = False
                    sub_menu = False
                elif str(choice).upper() == 'O':
                    if not storage_set:
                        print "Storage list is empty"
                    else:
                        #new sub menu for choice files profile
                        sub_sub_menu   = True
                        sub_choice_set = set()
                        data_set       = set()
                        while sub_sub_menu:
                            print "\nAll files will be saved in: "
                            print "/" * 16
                            [printf("* " + x.name) for x in storage_set]
                            print "/" * 16, '\n'
                            num = 1
                            menu_dict = {}
                            print "Profiles list: "
                            for profile in CONFIG["DATA"].keys():
                                print str(num) + ". " + profile + " ",
                                if int(num) in sub_choice_set:
                                    print "+"
                                    data_set.add(profile)

                                else:
                                    print " "
                                menu_dict[num] = profile
                                num += 1
                            print "\n0." + " Select all storages\n", "(O)k\n", "(V)iev\n", "(Q)uit\n", "(E)xit"
                            print "-" * 16
                            choice = raw_input('Choice action from menu: ')
                            if choice.upper() == 'Q':
                                sub_sub_menu = False
                            elif choice.upper() == 'E':
                                menu_run = False
                                sub_menu = False
                                sub_sub_menu = False
                            elif choice.upper() == "V":
                                choice = raw_input("\n Enter Profile number: ")
                                if int(choice) > 0 and int(choice) <= len(menu_dict.keys()):
                                    for file in CONFIG["DATA"][menu_dict[int(choice)]]:
                                        print file
                            elif not choice.isalpha() and int(choice) > 0 and int(choice) < num:
                                sub_choice_set.add(int(choice))

                            elif choice == '0':
                                [sub_choice_set.add(x) for x in xrange(1, num)]
                            elif str(choice).upper() == 'O':
                                for profile in data_set:
                                    file_obj_list = [Data(x) for x in CONFIG["DATA"][profile]]
                                    for storage in storage_set:
                                        if storage.save(profile, file_obj_list):
                                            print "error"  # this place for error log
                                print "BACKUP FINISH!!!!"
                                sub_menu = False
                                sub_sub_menu = False
                            else:
                                print "There no " + choice + " in menu"
                else:
                     print "There no " + choice + " in menu"

        elif choice.upper() == 'R':
        #menu branch for non correct enter
            sub_menu = True
            storage = Storage(CONFIG['STORAGES']['STOR_1']) #''
            date = ''
            profile = ''
            time = ''
            files  = ''
            while sub_menu:
                if storage and date: storage.set_current_date(date)
                if not storage:
                    print "Set storage"
                    [printf(x) for x in CONFIG['STORAGES'].keys()]
                    current_storage = raw_input("Example: "+ CONFIG['STORAGES'].keys()[0] + "\nEnter Storage name: ")
                    if current_storage in set(CONFIG['STORAGES'].keys()):
                        storage = Storage(CONFIG['STORAGES'][current_storage])
                    elif current_storage.upper() == 'Q':
                        sub_menu = False
                    else:
                        print "No storage with name: " + current_storage
                elif not date:
                    print "Set date"
                    [printf(x) for x in storage.get_date_folders()]
                    current_date = raw_input("Example: "+ storage.get_date_folders()[0] + "\nEnter date: ")
                    if current_date in set(storage.get_date_folders()):
                        date = current_date
                    elif current_date.upper() == 'Q':
                        sub_menu = False
                    else:
                        print "No date with name: " + current_date

                elif not profile:
                    print "Set profile"
                    [printf(x) for x in storage.get_profile_folders()]
                    current_profile = raw_input("Example: "+ storage.get_profile_folders()[0] + "\nEnter Profile name: ")
                    if current_profile in set(storage.get_profile_folders()):
                        profile = current_profile
                    elif current_profile.upper() == 'Q':
                        sub_menu = False
                    else:
                        print "No Profile with name: " + current_profile

                elif not time:
                    print "Set time"
                    [printf(x) for x in storage.get_time_folders(profile)]
                    current_time = raw_input("Example: " + storage.get_time_folders(profile)[0] + "\nEnter time: ")
                    if current_time in set(storage.get_time_folders(profile)):
                        time = current_time
                    elif current_time.upper() == 'Q':
                        sub_menu = False
                    else:
                        print "No time with name: " + current_time
                elif not files:
                    sub_sub_menu = True
                    files_set = set([Data(x) for x in CONFIG["DATA"][profile]])
                    restore_set = set()
                    while sub_sub_menu:
                        num = 1
                        menu_dict = {}
                        for file in files_set:
                            print str(num) + ". " + file.get_name(),
                            if file in restore_set:
                                print "+"
                            else:
                                print ""
                            menu_dict[num] = file
                            num += 1
                        print "\n"
                        print "0." + " Select files\n", "(O)k - restore!\n", "(Q)uit\n", "(E)xit\n"
                        choice = raw_input("Enter your choice: ")
                        if choice.upper() == 'Q':
                            sub_menu = False
                            sub_sub_menu = False
                        elif choice.upper() == 'E':
                            menu_run = False
                            sub_menu = False
                            sub_sub_menu = False
                        elif not choice.isalpha() and int(choice) > 0 and int(choice) < num:
                            restore_set.add(menu_dict[int(choice)])
                        elif choice == '0':
                             restore_set = files_set
                        elif str(choice).upper() == 'O':
                            if files_set:
                                if storage.restore(date, profile, time, files_set):
                                    print "error restore"
                                else:
                                    print "Restore finish"
                                    sub_menu = False
                                    sub_sub_menu = False

                        else:
                            print "The are no " + choice + " in menu"

        else:
            print "The are no " + choice + " in menu"
