from core.fern import *

############# WEP/WPA GLOBAL VARIABLES #################
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

################### DIRECTORY GLOBAL VARIABLES ##################
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
def set_key_entries(arg,arg1,arg2,arg3,arg4):
    connection = sqlite3.connect('key-database/Database.db')
    query = connection.cursor()
    query.execute("insert into keys values ('%s','%s','%s','%s','%s')"%(str(arg),str(arg1),str(arg2),str(arg3),str(arg4)))
    connection.commit()
    connection.close()

########## GENERIC GLOBAL READ/WRITE FUNCTIONS ###############
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


################## TOOL BOX VARIABLES #######################

# FERN GEOLOCATORY MAC-ADDRESS TRACKER VARIABLES

#
# Error Strings
#
database_null_error = 'There are currently no access points inserted into the database,\
Access points are added automatically after a successful attack,\
alternatively you can insert access point details manually using the\
 "Key Database" section of the main window,you can also input mac-addresses directly.\
'

invalid_mac_address_error = 'The Mac address inserted is invalid, \
a valid mac address has 6 segment with 2 hexadecimal values in each segment e.g 00:CA:56:12:8B:90'

#
# Html strings
#

html_network_timeout_error = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
<style type="text/css">
body,td,th {
	font-size: 12px;
}
</style>
</head>

<body>
<p><img src="file://%s/resources/map.png" alt="" width="108" height="87" /><strong> Fern GeoLocatory Mac Address Tracker
  </strong>
</p>
<p><font color="#FF0000">Network Timeout:</font></p>
<p>* The current network connection does not have access to the internet.</p>
<p>* Please check your internet connection to make sure its connected to the internet.</p>
<p>* Press the &quot;Track&quot; button when you're done.</p>
</body>
</html>
'''%(os.getcwd())

html_instructions_message = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
<style type="text/css">
body,td,th {
	font-size: 12px;
}
</style>
</head>

<body>
<p><img src="file://%s/resources/map.png" alt="" width="108" height="87" /> <strong>Fern GeoLocatory Mac Address Tracker </strong></p>
<p><font color=blue>Instructions:</font></p>
<p>* Fern Geolocatory Mac Address Tracker allows you track the geographical coordinates of wifi mac-addresses.</p>
<p>* The geographical co-ordinates are retrived and the corresponding maps are displayed on this very area you are reading from.</p>
<p>* Mac-addresses can either be inserted from the list of mac-addresses in &quot;Fern Key Database&quot; or otherwise inserted manually.</p>
<p>* You can insert mac-addresses manually by using the &quot;Insert Mac Address&quot; radio button then inputing it into the combo-box.</p>
</body>
</html>
'''%(os.getcwd())

