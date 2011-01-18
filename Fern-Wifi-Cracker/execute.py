import os
import sys
import commands
from PyQt4 import QtGui,QtCore
from main_window import *

class mainwindow(QtGui.QDialog,Ui_Dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        #
        # Checks privilegde level - for aircrack-ng suite needs those
        #
        if os.getenv('LOGNAME','none').lower() == 'root':
            resolution = str(commands.getstatusoutput('xrandr | grep \'current\''))
            resolution_process = resolution.replace(',','\n')
            resolution_process2 = resolution_process.splitlines()
            resolution_process3 = resolution_process2[2].strip(' current')
            original_resolution = resolution_process3.replace(' x ','x')
            if 'display.txt' in os.listdir('/tmp'):
                os.system('rm -r /tmp/display.txt')
                log_display = open('/tmp/display.txt','a+')
                log_display.write(original_resolution)
                log_display.close()
            else:
                log_display = open('/tmp/display.txt','a+')
                log_display.write(original_resolution)
                log_display.close()
            commands.getstatusoutput('xrandr -s 800x600')
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
run = mainwindow()
app.exec_()


