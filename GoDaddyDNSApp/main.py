from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

from future.utils import raise_
from future.utils import raise_with_traceback
from future.utils import raise_from
from future.utils import iteritems

import os
from builtins import FileExistsError

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5 import QtGui
import sys
#from MainWindow import Ui_MainWindow

from godaddypy import Client, Account
from godaddypy.client import BadResponse 
import simplejson as json
from pathlib import Path
#Key
PUBLIC_KEY = "9ELgAwGRufU_GCCa1CsM7JK785DqWGHAjF"
# Secret
SECRET_KEY =  "GCCbu9i9h2QCK2zW6VdzvZ"
APPNAME = "GoDaddyDNSApp"

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import qApp
from PyQt5.QtCore import QSize

from ui.dnsquickedit import Ui_DNSQuickEdit
#from ui.configwindow import Ui_ConfigWindow
from ui.apikeyentry import Ui_ApiKeyEntry
from ui.about import Ui_AboutDialog
from resources import get_settings_path

class DNSRecord(object):
    
    def __init__(self, client, domain=None, host=None, data=None, 
                 type=None, priority=None,ttl=None,
                 ):
        self.client = client
        self.domain = domain
        self.host = host
        self.data = data
        self.type = type
        self.priority = priority
        self.ttl = ttl
        
        
    def add(self):
        pass
    
    def delete(self):
        pass
    
    def update(self):
        pass
    
    def update_or_add(self):
        pass
    
     
class ARecordHandler(DNSRecord):
    
    def add(self):
        self.client.add_record(self.domain, {'name':  self.host , 
                                        'ttl': int(self.ttl), 
                                        'data': self.data, 
                                        'type': 'A'})
    
    def add_or_update(self):
        #if a record already exists, then we need to delete it first. 
        res = self.client.get_records(self.domain, record_type='A', name = self.host)
        for entry in res:
            self.client.delete_records(self.domain, name=self.host)
        self.add()
        
    
class CNAMERecordHandler(DNSRecord):
    
    def add(self):
        self.client.add_record(self.domain,{'name': self.host, 
                                            'ttl': int(self.ttl), 
                                            'data': self.data, 
                                            'type': 'CNAME'})
        
class MXRecordHandler(DNSRecord):
    
    def add(self):
        self.client.add_record(self.domain,{'name': self.host, 
                                            'data': self.data, 
                                            'ttl': int(self.ttl), 
                                            'type': 'MX',
                                            'priority': int(self.priority)})        
        
class DNSQuickEditWindow(QMainWindow, Ui_DNSQuickEdit):
    
    def __init__(self, client):
        
        super(DNSQuickEditWindow, self).__init__()
        self.client = client
        self.ui = Ui_DNSQuickEdit()
        self.ui.setupUi(self)
        self.ui.addRecordButton.clicked.connect(self.onAddRecordButtonClicked)
        self.ui.updateRecordButton.clicked.connect(self.onAddOrUpdateRecordButtonClicked)        
        self.ui.recordTypeDropDown.currentIndexChanged.connect(self.onRecordTypeDropdownChanged)
      
    def onRecordTypeDropdownChanged(self, event):
        text = self.ui.recordTypeDropDown.currentText()
        if text == "CNAME":
            #cname does not require priority
            self.ui.priorityDropDown.setEnabled(False)
        elif text == "A":
            self.ui.priorityDropDown.setEnabled(False)
        elif text == "MX":
            self.ui.priorityDropDown.setEnabled(True)
        
        
        
    def onAddRecordButtonClicked(self, event):
        self.handleRequest()

    def onAddOrUpdateRecordButtonClicked(self, event):
        self.handleRequest(update=True)
    
    def handleRequest(self,  update=False):
        
        type = self.ui.recordTypeDropDown.currentText()
        domain = self.ui.domainDropDown.currentText()
        host = self.ui.hostEdit.text()
        data = self.ui.pointsToEdit.text()
        handlerName = "{}RecordHandler".format(type)
        priority = self.ui.priorityDropDown.currentText()
        ttl = self.ui.ttlDropDown.currentText()
        handlerClass = globals()[handlerName]
        handlerInstance = handlerClass(self.client, 
                                       host = host,
                                       domain=domain, 
                                         data=data, 
                                       type=type, 
                                       priority=priority,
                                       ttl=ttl)
        
        msg = "Processing request..."
        self.ui.statusBar.showMessage(msg, 3000)
        if update:
            handlerInstance.add_or_update()
        else:
            handlerInstance.add()
    
        msg = "{}.{} points to {}".format(host, domain, data)
        self.ui.statusBar.showMessage(msg, 3000)
    
    # Override closeEvent, to intercept the window closing event
    def closeEvent(self, event):
        event.ignore()
        self.hide()
      
        #self.tray_icon.showMessage(
          #"Tray Program",
            #"Application was minimized to Tray",
             #QSystemTrayIcon.Information,
             #2000
      #)   
      
class AboutWindow(QMainWindow, Ui_AboutDialog):
    def __init__(self,parent=None):
        super(AboutWindow, self).__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.parent = parent
        
    def closeEvent(self,event):
        event.ignore()
        self.hide()
      
class ApiKeyEntryWindow(QMainWindow, Ui_ApiKeyEntry):
    def __init__(self):
        super(ApiKeyEntryWindow, self).__init__()
        self.ui = Ui_ApiKeyEntry()
        self.ui.setupUi(self)
        
        self.ui.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.ui.cancelButton.clicked.connect(self.onCancelButtonClicked)
        
        settings_dir, config_pathname = self.get_config_pathname()
        try:
            if settings_dir.exists():
                with open(config_pathname.as_posix(), "r") as f:
                    s = f.read()
                    d = json.loads(s)
                    
                    self.ui.publikKeyEdit.setText(d.get("PUBLIC_KEY"))
                    self.ui.secretKeyEdit.setText(d.get("SECRET_KEY"))
            else:
                os.makedirs(settings_dir.as_posix())        
                
        except json.errors.JSONDecodeError as e:
            print("JSON Decode error")
        except Exception as e:
            print("Unhjandled exception")
            
    #def closeEvent(self, event):
    #    self.hide()
    #    event.accept()
     
    def onSaveButtonClicked(self, event):
        settings_dir, config_pathname = self.get_config_pathname()
        if not settings_dir.exists():
            os.makedirs(settings_dir.as_posix())
            
        public_key = self.ui.publikKeyEdit.text()
        secret_key = self.ui.secretKeyEdit.text()
        
        api_key_dict = { "PUBLIC_KEY": public_key, 
                         "SECRET_KEY": secret_key}
            
        with open(config_pathname.as_posix(), "w") as f:
            f.write(json.dumps(api_key_dict))   
        self.hide()

    def get_config_pathname(self):
        settings_dir = get_settings_path(APPNAME)
        config_pathname = Path(settings_dir, "config.json")
        return settings_dir, config_pathname
        
    def onCancelButtonClicked(self, event):
        self.hide()
      
class MainWindow(QMainWindow):
    """
    This window is never but it does host the tray menu and is where most of the 
    program logic is in.
    """
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
    
        '''
            Define and add steps to work with the system tray icon
            show - show window
            hide - hide window
            exit - exit from application
        '''
         
        #config_action = QAction("Config", self)
        update_action = QAction("QuickDNSUpdate", self)
        config_action = QAction("Configuration", self)
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        about_action = QAction("About", self)
       #config_action.triggered.connect(self.onConfig)
        
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)   
        config_action.triggered.connect(self.onConfigMenuClicked)
        about_action.triggered.connect(self.aboutClickedHandler)
        update_action.triggered.connect(self.onDNSUpdateMenuIconClicked)
        
        tray_menu = QMenu()
        
        tray_menu.addAction(update_action)
        #tray_menu.addAction(show_action)
        #tray_menu.addAction(hide_action)
        tray_menu.addAction(config_action)
        tray_menu.addAction(about_action)
        tray_menu.addAction(quit_action)
    
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.onTrayIconActivated)
        self.tray_icon.show()   
    
        self.quick_edit_window = None
        self.api_key_entry_window = None
        self.about_window = None
        
        self.about_window = AboutWindow(self)        
    
    def onTrayIconActivated(self,activationReason):

        """" 
        enum QSystemTrayIcon::ActivationReason
        This enum describes the reason the system tray was activated.

        Constant	Value	Description
        QSystemTrayIcon::Unknown	0	Unknown reason
        QSystemTrayIcon::Context	1	The context menu for the system tray entry was requested
        QSystemTrayIcon::DoubleClick	2	The system tray entry was double clicked.
        Note: On macOS, a double click will only be emitted if no context menu is set, since the menu opens on mouse press

        Constant	Value	Description
        QSystemTrayIcon::Trigger	3	The system tray entry was clicked
        QSystemTrayIcon::MiddleClick	4	The system tray entry was clicked with the middle mouse button

        """
        if self.quick_edit_window is None:
            #it does not exist yet. So create it.
            self.showQuickEditWindow()
            return
        
        elif activationReason == 3:
            if self.quick_edit_window.isHidden():
                self.quick_edit_window.show()
            else:
                self.quick_edit_window.hide()
        
        
    def loadApiKey(self):
        name="GoDaddyDNSApp"
        settings_dirs = get_settings_path(name)
        import os
        fname = os.path.join(path)
        
    def aboutWindowClosed(self, event):
        self.hide()
        
    def aboutClickedHandler(self, event):
   
        self.about_window.show()
        
        #Now restore to how it was
        #if hidden_state == True:
        #    self.hide()
            
    def onDNSUpdateMenuIconClicked(self, event):
        #Show the dnsquickedit gui. 
     
        self.showQuickEditWindow()

    def showQuickEditWindow(self):
        if self.quick_edit_window == None:
            settings_dir, config_pathname = self.get_config_pathname()
            try:
                with open(config_pathname.as_posix(), "r") as f:
                    s = f.read()
                    d = json.loads(s)            
                    my_acct = Account(api_key=d.get("PUBLIC_KEY"), 
                                      api_secret=d.get("SECRET_KEY"))
                    client = Client(my_acct)                                 
                    
            except Exception as e:
                #Failed to load the configs. 
                print("Error Occured", e)
                client = None
                
            self.quick_edit_window = DNSQuickEditWindow(client)
                
        #move the window to bottom right.
        screenGeometry = QApplication.desktop().availableGeometry()
        screenGeo = screenGeometry.bottomRight()
    
        self.quick_edit_window.move(screenGeo)
        self.quick_edit_window.show()
        msgGeo = self.quick_edit_window.frameGeometry()    
        msgGeo.moveBottomRight(screenGeo)
        self.quick_edit_window.move(msgGeo.topLeft())  # msgGeo.topLeft()
        
    def get_config_pathname(self):
        settings_dir = get_settings_path(APPNAME)
        config_pathname = Path(settings_dir, "config.json")
        return settings_dir, config_pathname
    
    def onConfigMenuClicked(self, event):
        if self.api_key_entry_window == None:
            self.api_key_entry_window = ApiKeyEntryWindow()
        self.api_key_entry_window.show()
        
    def onClose(self, event):
        print("Close event")
        
def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.svg'))
    window = MainWindow()
    window.hide()
    app.exec_()

if __name__ == "__main__":
    
    import ctypes
    myappid = 'zinnianet.dns.quickedit.1' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)    
    main()


"""
>>> from godaddypy import Client, Account
>>>
>>> my_acct = Account(api_key='PUBLIC_KEY', api_secret='SECRET_KEY')
>>> client = Client(my_acct)
>>>
>>> client.get_domains()
['domain1.example', 'domain2.example']
>>>
>>> client.get_records('domain1.example', record_type='A')
[{'name': 'dynamic', 'ttl': 3600, 'data': '1.1.1.1', 'type': 'A'}]
>>>
>>> client.update_ip('2.2.2.2', domains=['domain1.example'])
True|
>>>
>>> client.get_records('domain1.example')
[{'name': 'dynamic', 'ttl': 3600, 'data': '2.2.2.2', 'type': 'A'}, {'name': 'dynamic', 'ttl': 3600, 'data': '::1',
'type': 'AAAA'},]
>>>
>>> client.get_records('apple.com', record_type='A', name='@')
[{u'data': u'1.2.3.4', u'type': u'A', u'name': u'@', u'ttl': 3600}]
>>>
>>> client.update_record_ip('3.3.3.3', 'domain1.example', 'dynamic', 'A')
True
>>>
>>> client.add_record('apple.com',{'name': 'dynamic', 'ttl': 3600, 'data': '2.2.2.2', 'type': 'A'}
True
>>>
>>> client.delete_records(dom, name='test')
True

"""