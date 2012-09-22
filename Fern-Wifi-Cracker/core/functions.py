import os
import re
import sqlite3
import commands
import subprocess

################### DATABASE INSERTION FUNCTIONS ##############
#
# Create database if it does not exist
#
def database_create():
    temp = sqlite3.connect(os.getcwd() + '/key-database/Database.db')                 # Database File and Tables are created Here
    temp_query = temp.cursor()
    temp_query.execute('''create table if not exists keys \
                            (access_point text,mac_address text,encryption text,key text,channel int)''')
    temp.commit()
    temp.close()


#
# Add keys to Database with this function
#

def upgrade_database():
    connection = sqlite3.connect('key-database/Database.db')
    query = connection.cursor()
    query.execute("select * from keys")

    if(len(query.description) < 5):
        temp_backup = query.fetchall()
        query.execute("drop table keys")
        query.execute('''create table keys (access_point text,mac_address text,encryption text,key text,channel int)''')
        for values in temp_backup:
            query.execute("insert into keys values ('%s','%s','%s','%s','%s')"%(values[0],str(),values[1],values[2],values[3]))
    connection.commit()
    connection.close()



def set_key_entries(arg,arg1,arg2,arg3,arg4):
    upgrade_database()
    connection = sqlite3.connect('key-database/Database.db')
    query = connection.cursor()
    sql_code = "select key from keys where mac_address ='%s' and encryption = '%s'"
    query.execute(sql_code % (str(arg1),str(arg2)))
    result = query.fetchall()
    if(result):
        sql_code_2 = "update keys set access_point = '%s',encryption = '%s',key = '%s',channel = '%s' where mac_address = '%s'"
        query.execute(sql_code_2 % (str(arg),str(arg2),str(arg3),str(arg4),str(arg1)))
    else:
        query.execute("insert into keys values ('%s','%s','%s','%s','%s')"%(str(arg),str(arg1),str(arg2),str(arg3),str(arg4)))
    connection.commit()
    connection.close()



def get_key_from_database(mac_address,encryption):
    cracked_key = str()
    upgrade_database()
    sql_code = "select key from keys where mac_address ='%s' and encryption = '%s'"
    connection = sqlite3.connect('key-database/Database.db')
    query = connection.cursor()
    query.execute(sql_code % (mac_address,encryption))
    result = query.fetchall()
    if(result):
        cracked_key = str(result[0][0])
    return(cracked_key)


def is_already_Cracked(mac_address,encryption):
    sql_code = "select key from keys where mac_address ='%s' and encryption = '%s'"
    connection = sqlite3.connect('key-database/Database.db')
    query = connection.cursor()
    query.execute(sql_code % (mac_address,encryption))
    result = query.fetchall()
    if(result):
        return(True)
    return(False)



def fern_database_query(sql_query):
    connection = sqlite3.connect('key-database/Database.db')
    query = connection.cursor()
    query.execute(sql_query)
    output = query.fetchall()
    connection.commit()
    connection.close()
    return(output)

########## GENERIC GLOBAL READ/WRITE FUNCTIONS ###############
#
# Some globally defined functions for write,copy and read tasks
#
def reader(arg):
    open_ = open(arg,'r+')
    read_file = open_.read()
    return read_file

def write(arg,arg2):
    open_ = open(arg,'a+')
    open_.write(arg2)
    open_.close()

def remove(arg,arg2):
    commands.getstatusoutput('rm -r %s/%s'%(arg,arg2))  #'rm - r /tmp/fern-log/file.log



########## GENERAL SETTINGS FUNCTION #########################

def create_settings(object_name,value):
    string = ''
    if value:
        last_settings = open('fern-settings/general_settings.dat','r')
        file_read = last_settings.read()
        last_settings.close()
        os.remove('fern-settings/general_settings.dat')
        all_files = file_read.splitlines()
        for iterate in all_files:
            if object_name in iterate:
                string += iterate
                old_settings_number = all_files.index(string)
                all_files.pop(old_settings_number)
        all_files.append('%s = %s'%(object_name,value))
        file_input_settings = open('fern-settings/general_settings.dat','a+')
        for settings in all_files:
            file_input_settings.write('%s\n'%(settings))
        file_input_settings.close()



def read_settings(object_name):
    target_variable = ''
    settings_file = open('fern-settings/general_settings.dat','r')
    settings_file_process = settings_file.read()
    settings_file_process2 = settings_file_process.splitlines()
    for iterate in settings_file_process2:
        if object_name in iterate:
            target_variable += iterate
    return str(target_variable.split()[2])



def remove_setting(object_name):
    settings_file = open('fern-settings/general_settings.dat','r')
    settings_file_process = settings_file.read()
    settings_file_process2 = settings_file_process.splitlines()
    regex = re.compile(object_name)
    for settings in enumerate(settings_file_process2):
        if re.match(regex,object_name):
            settings_file_process2.pop(settings[0])
    os.remove('fern-settings/general_settings.dat')
    file_input_settings = open('fern-settings/general_settings.dat','a+')
    for settings in settings_file_process2:
        file_input_settings.write('%s\n'%(settings))
    file_input_settings.close()



def create_settings_file():
    if not os.path.exists(os.getcwd() + '/fern-settings/general_settings.dat'):
        setting_file = open(os.getcwd() + '/fern-settings/general_settings.dat','a+')
        setting_file.close()


def settings_exists(object_name):
    create_settings_file()
    settings_file = open('fern-settings/general_settings.dat','r')
    regex = re.compile(object_name)
    if re.search(regex,settings_file.read()):
        return True
    else:
        return False


################# MAC Address Validator ######################

def Check_MAC(mac_address):
    hex_digits = re.compile('([0-9a-f]{2}:){5}[0-9a-f]{2}',re.IGNORECASE)
    if re.match(hex_digits,mac_address):
        return(True)
    return(False)


#################   FILE LINE COUNTER ########################

def line_count(filename):
    count = 0
    files = open(filename,'r')
    for line in files:
        count += 1
    files.close()
    return(count)

######################## Font settings #######################
def font_size():
	font_settings = open('%s/.font_settings.dat'%(os.getcwd()),'r+')
	font_init = font_settings.read()
	return int(font_init.split()[2])


###################### Process Terminate ######################






