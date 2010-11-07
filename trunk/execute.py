import os
import sys
from PyQt4 import QtGui,QtCore
from main_window import *

class mainwindow(QtGui.QDialog,Ui_Dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        #
        # Checks privilegde level - for aircrack-ng suite needs those
        #
        if os.getenv('LOGNAME','none').lower() == 'root':
            variable = sys.argv[0]
            direc = variable.replace('execute.py',"")
            os.system('cd %s \n python fern.py'%(direc))
        else:
            QtGui.QMessageBox.warning(self,"Insufficient Priviledge","Aircrack and other dependencies need root priviledge to function, Please run application as root")
            sys.exit()
        
   

app = QtGui.QApplication(sys.argv)
run = mainwindow()
run.show()
app.exec_()


