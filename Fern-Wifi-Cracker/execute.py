import os
import sys
import shutil
import commands
from PyQt4 import QtGui


def initialize():
    'Set Working directory'
    if 'core' in os.listdir(os.getcwd()):
        place_update_png(os.getcwd())
        create_directory()
    else:
        variable = sys.argv[0]
        direc = variable.replace('execute.py',"")
        os.chdir(direc)
        place_update_png(os.getcwd())
        create_directory()


def create_directory():
    'Create directories and database'

    if not os.path.exists('fern-settings'):
        os.mkdir('fern-settings')                               # Create permanent settings directory
    if not os.path.exists('key-database'):                      # Create Database directory if it does not exist
        os.mkdir('key-database')



def place_update_png(directory):
    png_files = ['1295905972_tool_kit.png','1295906241_preferences-desktop-font.png','mac_address.png']
    for png_file in png_files:
        if png_file not in os.listdir(directory + os.sep + 'resources'):
            try:
                shutil.copyfile('/tmp/Fern-Wifi-Cracker/resources/' + png_file,directory + '/resources/' + png_file)
            except IOError:
                pass

def cleanup():
    'Kill all running processes'
    commands.getstatusoutput('killall airodump-ng')
    commands.getstatusoutput('killall aircrack-ng')
    commands.getstatusoutput('killall airmon-ng')
    commands.getstatusoutput('killall aireplay-ng')



initialize()
from core import *
variables.database_create()
from gui import *


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    run = fern.mainwindow()
    run.show()
    app.exec_()
    cleanup()


