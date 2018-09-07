import core
from PyQt5.QtWidgets import *
from gui.database import *
from core.functions import *
from core.variables import *

#
#  Class for Database key entries
#
class database_dialog(QtWidgets.QDialog,database_ui):
    update_database_label_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.display_keys()

        self.insert_button.clicked.connect(self.insert_row)
        self.delete_button.clicked.connect(self.delete_row)
        self.save_button.clicked.connect(self.save_changes)




    def display_keys(self):
        connection = sqlite3.connect('key-database/Database.db')
        query = connection.cursor()
        query.execute('''select * from keys''')
        items = query.fetchall()
        query.close()

        for iterate in range(len(items)):              # Update QTable with entries from Database and

            tuple_sequence = items[iterate]

            if len(tuple_sequence) == 4:                      # If we have access point mac-address absent
                access_point_var = tuple_sequence[0]
                mac_address_var = '\t'
                encryption_var = tuple_sequence[1].upper()
                key_var = tuple_sequence[2]
                channel_var = tuple_sequence[3]
            else:
                access_point_var = tuple_sequence[0]
                mac_address_var = tuple_sequence[1]
                encryption_var = tuple_sequence[2].upper()
                key_var = tuple_sequence[3]
                channel_var = tuple_sequence[4]

            self.key_table.insertRow(iterate)

            access_point_display = QtWidgets.QTableWidgetItem()
            mac_address_display = QtWidgets.QTableWidgetItem()
            encryption_display = QtWidgets.QTableWidgetItem()
            key_display = QtWidgets.QTableWidgetItem()
            channel_display = QtWidgets.QTableWidgetItem()

            access_point_display.setText(QtCore.QCoreApplication.translate("Dialog", "%s"%(access_point_var), None, 0))
            self.key_table.setItem(iterate,0,access_point_display)

            mac_address_display.setText(QtCore.QCoreApplication.translate("Dialog", "%s"%(mac_address_var), None, 0))
            self.key_table.setItem(iterate,1,mac_address_display)

            encryption_display.setText(QtCore.QCoreApplication.translate("Dialog", "%s"%(encryption_var), None, 0))
            self.key_table.setItem(iterate,2,encryption_display)

            key_display.setText(QtCore.QCoreApplication.translate("Dialog", "%s"%(key_var), None, 0))
            self.key_table.setItem(iterate,3,key_display)

            channel_display.setText(QtCore.QCoreApplication.translate("Dialog", "%s"%(channel_var), None, 0))
            self.key_table.setItem(iterate,4,channel_display)



    def insert_row(self):
        self.key_table.insertRow(0)

    def delete_row(self):
        current_row = int(self.key_table.currentRow())
        self.key_table.removeRow(current_row)

    def save_changes(self):
        row_number = self.key_table.rowCount()
        fern_database_query('''delete from keys''')    # Truncate the "keys" table

        for controller in range(row_number):
            try:
                access_point1 = QtWidgets.QTableWidgetItem(self.key_table.item(controller,0))   # Get Cell content
                mac_address1 = QtWidgets.QTableWidgetItem(self.key_table.item(controller,1))
                encryption1 = QtWidgets.QTableWidgetItem(self.key_table.item(controller,2))
                key1 = QtWidgets.QTableWidgetItem(self.key_table.item(controller,3))
                channel1 = QtWidgets.QTableWidgetItem(self.key_table.item(controller,4))

                access_point = str(access_point1.text())                                    # Get cell content text
                mac_address = str(mac_address1.text())
                encryption2 = str(encryption1.text())
                encryption = encryption2.upper()
                key = key1.text()
                channel = channel1.text()

                if not (bool(access_point) and bool(mac_address) and bool(encryption) and bool(key) and bool(channel)):
                    raise(TypeError)

                set_key_entries(access_point,mac_address,encryption,key,channel)       # Write enrties to database

            except(TypeError):
                QtWidgets.QMessageBox.warning(self,"Empty Database Entries",\
                    "There are some fields with whitespaces,Please enter empty spaces with Access Point related data")
                break

        self.update_database_label_signal.emit()


