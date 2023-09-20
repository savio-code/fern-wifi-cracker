#!/usr/bin/env python

import os
import sys
import time
import importlib

def install_prerequisites():
    modules = {"scapy":"scapy", "PyQt5":"pyqt5", "csv":"csv"}
    os.system("pip3 install " + " ".join(modules.values()))

if sys.version_info.major <= 2:
    try:
        from PyQt5 import QtWidgets
        python_version = sys.version.split()[0]
        QtWidgets.QMessageBox.warning(None,"Python 3 Required","You have executed the program using Python {0}.\n\nPlease use Python 3 or above to run this program".format(python_version))
    except ImportError:
        print("Please use Python 3 to execute this program")
    finally:
        sys.exit(-1)

install_prerequisites()

from PyQt5 import QtCore, QtGui, QtWidgets

def initialize():
    'Set Working directory'
    os.chdir(os.path.dirname(sys.argv[0]) or '.') # Change current working directory
    if not os.path.exists('fern-settings'):
        os.mkdir('fern-settings')
    if not os.path.exists('key-database'):
        os.mkdir('key-database')

    os.system("export QT_X11_NO_MITSHM=1")      # Bug fixes [https://github.com/savio-code/fern-wifi-cracker/issues/113]

def restore_files():
    '''Fern 1.2 update algorithm fails to update the new version files 
        therefore this piece of code corrects that defect when running 
        the program after an update from 1.2'''
    update_directory = '/tmp/Fern-Wifi-Cracker/'
    for old_file in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(), old_file)) and old_file != '.font_settings.dat':
            os.remove(os.path.join(os.getcwd(), old_file))
    for old_directory in os.listdir(os.getcwd()):
        if os.path.isdir(os.path.join(os.getcwd(), old_directory)) and old_directory != 'key-database':
            shutil.rmtree(os.path.join(os.getcwd(), old_directory))
    for update_file in os.listdir(update_directory):        # Copy New update files to working directory 
        if os.path.isfile(os.path.join(update_directory, update_file)):
            shutil.copyfile(os.path.join(update_directory, update_file), os.path.join(os.getcwd(), update_file))
        else:
            shutil.copytree(os.path.join(update_directory, update_file), os.path.join(os.getcwd(), update_file))
    for new_file in os.listdir(os.getcwd()):
        os.chmod(os.path.join(os.getcwd(), new_file), 0o777)

def create_directory():
    'Create directories and database'
    if not os.path.exists('fern-settings'):
        os.mkdir('fern-settings')
    if not os.path.exists('key-database'):
        os.mkdir('key-database')

def cleanup():
    'Kill all running processes'
    os.system('killall airodump-ng aircrack-ng airmon-ng')

initialize()

if 'core' not in os.listdir(os.getcwd()):
    restore_files()


from core import *
functions.database_create()
from gui import *


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    run = fern.mainwindow()

    pixmap = QtGui.QPixmap("%s/resources/screen_splash.png" % (os.getcwd()))
    screen_splash = QtWidgets.QSplashScreen(pixmap, QtCore.Qt.WindowStaysOnTopHint)
    screen_splash.setMask(pixmap.mask())
    screen_splash.show()
    app.processEvents()

    time.sleep(3)

    screen_splash.finish(run)
    run.show()
    app.exec_()


cleanup()
sys.exit()
