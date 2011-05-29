from core.fern import *
#
# Network scan global variable
#
scan_control = 0
#
# Update checking loop (control variable)
#
updater_control = 0
xterm_setting = ''
#
# Wep Global variables
#
wep_details = {}
victim_mac = ''
victim_channel = ''
victim_access_point = ''
ivs_number = 0
WEP = ''
digit = 0
ivs_new = ivs_number + digit
#
# Wpa Global variables
#
wpa_details = {}
wpa_victim_mac_address = ''
wpa_victim_channel = ''
wpa_victim_access = ''
control = 0
current_word = ''
#
# Creating /tmp/ directory for logging of wireless information
#

direc = '/tmp/'
log_direc = 'fern-log'
tmp_direc = os.listdir(direc)                                    # list/tmp/
directory = os.getcwd()

#
# Create temporary log directory
#
if 'fern-log' in tmp_direc:
    commands.getstatusoutput('rm -r %s'%(direc + log_direc))    # Delete directory in /fern-log if it already exists in /tmp/
    os.mkdir(direc + log_direc)
else:
    os.mkdir(direc + log_direc)                                 # Create /tmp/fern-log/

#
# Create Sub Temporary directory in /tmp/fern-log
#
os.mkdir('/tmp/fern-log/WPA')                                     # Create /tmp/fern-log/WPA

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
def set_key_entries(arg,arg1,arg2,arg3,arg4):
    connection = sqlite3.connect('key-database/Database.db')
    query = connection.cursor()
    query.execute("insert into keys values ('%s','%s','%s','%s','%s')"%(str(arg),str(arg1),str(arg2),str(arg3),str(arg4)))
    connection.commit()
    connection.close()

#
# Some globally defined functions for write and read tasks
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

