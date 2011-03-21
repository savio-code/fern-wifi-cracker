import os
import sys
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
                os.system('python fern.py')
            else:
                variable = sys.argv[0]
                direc = variable.replace('execute.py',"")
                os.system('cd %s \n python fern.py'%(direc))
            commands.getstatusoutput('killall airodump-ng')
            commands.getstatusoutput('killall aircrack-ng')
            commands.getstatusoutput('killall airmon-ng')
            commands.getstatusoutput('killall aireplay-ng')
            sys.exit()

        else:
            QtGui.QMessageBox.warning(self,"Insufficient Priviledge","Aircrack and other dependencies need root priviledge to function, Please run application as root")
            sys.exit()



app = QtGui.QApplication(sys.argv)
run = initializing_interface()
app.exec_()


