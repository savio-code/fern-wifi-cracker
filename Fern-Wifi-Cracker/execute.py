import os
import sys
import shutil
import commands
from PyQt4 import QtGui,QtCore
from settings import *

class initializing_interface(QtGui.QDialog,settings):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        #
        # Checks privilegde level - for aircrack-ng suite needs those
        #
        if os.getenv('LOGNAME','none').lower() == 'root':
            if 'fern.py' in os.listdir(os.getcwd()):
                self.place_update_png(os.getcwd())
                os.system('python fern.py')
            else:
                variable = sys.argv[0]
                direc = variable.replace('execute.py',"")
                os.chdir(direc)
                self.place_update_png(os.getcwd())
                os.system('python fern.py')
            commands.getstatusoutput('killall airodump-ng')
            commands.getstatusoutput('killall aircrack-ng')
            commands.getstatusoutput('killall airmon-ng')
            commands.getstatusoutput('killall aireplay-ng')
            sys.exit()

        else:
            QtGui.QMessageBox.warning(self,"Insufficient Priviledge","Aircrack and other dependencies need root priviledge to function, Please run application as root")
            sys.exit()


    def place_update_png(self,directory):
        png_files = ['1295905972_tool_kit.png','1295906241_preferences-desktop-font.png','stop.png']
        for png_file in png_files:
            if png_file not in os.listdir(directory + os.sep + 'resources'):
                try:
                    shutil.copyfile('/tmp/Fern-Wifi-Cracker/resources/' + png_file,directory + '/resources/' + png_file)
                except IOError:
                    pass



app = QtGui.QApplication(sys.argv)
run = initializing_interface()
app.exec_()


