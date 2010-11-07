import os
import sys
import time
import thread
import subprocess
from PyQt4 import QtGui,QtCore
from main_window import *

class mainwindow(QtGui.QDialog,Ui_Dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)


       
        

    #
    # Checks privilegde level - for aircrack-ng suite needs those
    #

        if os.getenv('LOGNAME','none').lower() == 'root':
            pass
        else:
            QtGui.QMessageBox.warning(self,"Insufficient Priviledge","Aircrack and other dependencies need root priviledge to function, Please run application as root")
            sys.exit()
        
   


app = QtGui.QApplication(sys.argv)
run = mainwindow()
run.show()
app.exec_()
