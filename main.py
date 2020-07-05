'''
@author: baronsss
'''
import sys
import os
import subprocess
from PyQt5.QtWidgets import QMenuBar, QAction, QApplication, QWidget, QFileDialog, QTextEdit, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QDialog, QMessageBox
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import *
from configparser import ConfigParser

config = ConfigParser()
config.read('settings.ini')

class ThreadClass(QThread):
    text = pyqtSignal(str)
    def __init__(self, lista):
        
        QThread.__init__(self)
        self.lista = lista
        
    def run(self):
        aet = config.get('Settings', 'aet')
        aecName = config.get('Settings', 'aecName')
        aecHost = config.get('Settings', 'aecHost')
        aecPort = config.get('Settings', 'aecPort')
        for percorso in self.lista:
            command = f'storescu -v -aet {aet} -aec {aecName} {aecHost} {aecPort} "{percorso}" +sd'
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            line2=''
            while True:
                line = p.stdout.readline().rstrip()
                
                line2 = line2+'\n'+str(line)
                print(line2)
                self.text.emit(str(line2))
                if not line:
                    break
            
class DirectoryFinder(QThread):
    path = pyqtSignal(str)
    
    def __init__(self, percorso):
        
        QThread.__init__(self)
        self.percorso = percorso
    
    def run(self):
        for root, dirs, files in os.walk(self.percorso):
            files = os.listdir(str(root)) #returns a list of files in the given directory
            for filename in files:
                if filename.endswith((".dcm", "", ".ima", ".jpg", ".tiff", ".png", ".tif", ".DCM", ".IMA", ".JPG", ".PNG", ".TIFF", ".TIF")):
                    self.path.emit(str(root))
                    break

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'SSG - StoreScu with Gui'
        self.left = 550
        self.top = 300
        self.width = 640
        self.height = 480
        self.initUI()
        
    def initUI(self):
        #Window geometry
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #Layout containers
        self.layout = QVBoxLayout()
        self.layoutH = QHBoxLayout()
        #Menu bar
        self.mainMenu = QMenuBar()
        self.infoMenu = self.mainMenu.addMenu('Info')
        #Menu bar sub-sections
        self.aboutAction = QAction('About')
        self.aboutAction.setStatusTip('About')
        self.aboutAction.triggered.connect(self.openAboutDialog)
        #Add sub-section to menu bar section
        self.infoMenu.addAction(self.aboutAction)
        self.layout.addWidget(self.mainMenu)
        self.layout.addSpacing(20)
        
        #LABEL AET
        self.label = QLabel()
        self.label.setText('AET:')
        self.layoutH.addWidget(self.label)
        
        #LINE EDIT AET
        self.textAet = QLineEdit()
        self.textAet.setPlaceholderText('sender')
        self.layoutH.addWidget(self.textAet)
        
        #LABEL AEC
        self.label2 = QLabel()
        self.label2.setText('AEC:')
        self.layoutH.addWidget(self.label2)
        
        #LINE EDIT AEC nome
        self.textAecNome = QLineEdit()
        self.textAecNome.setPlaceholderText('receiver')
        self.layoutH.addWidget(self.textAecNome)
        
        #LINE EDIT AEC indirizzo
        self.textAecIndirizzo = QLineEdit()
        self.textAecIndirizzo.setPlaceholderText('hostname')
        self.layoutH.addWidget(self.textAecIndirizzo)
        
        #LINE EDIT AEC porta
        self.textAecPorta = QLineEdit()
        self.textAecPorta.setPlaceholderText('port')
        self.layoutH.addWidget(self.textAecPorta)
        
        self.layout.addLayout(self.layoutH)
        
        self.layoutH2 = QHBoxLayout()
        #Browse directory button
        self.buttonDirectory = QPushButton()
        self.buttonDirectory.setText('Browse')
        self.buttonDirectory.setFixedHeight(30)
        self.buttonDirectory.setFixedWidth(80)
        self.buttonDirectory.clicked.connect(self.selectDirectory)
        self.layoutH2.addWidget(self.buttonDirectory)
        
        self.textDirectory = QLineEdit()
        self.textDirectory.setFixedHeight(25)
        self.layoutH2.addWidget(self.textDirectory)
        
        self.layout.addLayout(self.layoutH2)
        
        self.layoutH3 = QHBoxLayout()
        self.layoutH3.addStretch(1)
        self.buttonOk = QPushButton()
        self.buttonOk.setText('OK')
        self.buttonOk.clicked.connect(self.trigger)
        self.layoutH3.addWidget(self.buttonOk)
        
        self.buttonStop = QPushButton()
        self.buttonStop.setText('Stop')
        self.buttonStop.clicked.connect(self.stop)
        self.buttonStop.setEnabled(False)
        self.layoutH3.addWidget(self.buttonStop)
        
        self.layout.addLayout(self.layoutH3)
        
        self.layout.addSpacing(150)
        
        self.textEdit = QTextEdit()
        self.layout.addWidget(self.textEdit)
        
        self.setLayout(self.layout)
        self.show()
    
    def openAboutDialog(self):
        self.aboutDialog = QDialog()
        text = QLabel("Created and Developed by Alessio Barone\ninfo.alessiobarone@gmail.com\ngithub.com/baronsss", self.aboutDialog)
        text.move(50,50)
        self.aboutDialog.setWindowTitle("About me")
        self.aboutDialog.setWindowModality(Qt.ApplicationModal)
        self.aboutDialog.setGeometry(650, 400, 500, 150)
        self.aboutDialog.show()
    
    def trigger(self):
        self.buttonStop.setEnabled(True)
        
        aet=self.textAet.text()
        aecName=self.textAecNome.text()
        aecHost=self.textAecIndirizzo.text()
        aecPort=self.textAecPorta.text()
        percorso = self.textDirectory.text()
        percorso=percorso.replace('/', '\\') #Replace of separators, escaping Unicode escape ;)
        config.set('Settings', 'aet', aet)
        config.set('Settings', 'aecName', aecName)
        config.set('Settings', 'aecHost', aecHost)
        config.set('Settings', 'aecPort', aecPort)
        config.set('Settings', 'percorso', percorso)
        
        with open('settings.ini', 'w') as config_file:
            config.write(config_file)
        
        self.threadclass = ThreadClass(self.lista)
        self.threadclass.start()
        self.threadclass.text.connect(self.updatetext)
    
    def stop(self):
        self.threadclass.terminate()
        self.threadclass.deleteLater()
        self.buttonStop.setEnabled(False)
    
    def updatetext(self, line):
        self.textEdit.setText(line)
        cursor = QTextCursor(self.textEdit.document())
        self.textEdit.setTextCursor(cursor)
        self.textEdit.moveCursor(QTextCursor.End)
    
    def selectDirectory(self):
        self.percorso = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if self.percorso:
            print(self.percorso)
            self.textDirectory.setText(self.percorso)
            self.percorso=self.percorso.replace('/', '\\')
            self.setEnabled(False)
            
            self.d = QDialog()
            text = QLabel("Loading directories...", self.d)
            text.move(50,50)
            self.d.setWindowTitle("Wait...")
            self.d.setWindowModality(Qt.ApplicationModal)
            self.d.setGeometry(700, 450, 250, 150)
            self.d.show()
            
            self.lista = []
            
            self.listaThread = DirectoryFinder(self.percorso)
            self.listaThread.finished.connect(self.finishDirectoryFinder)
            self.listaThread.start()
            self.listaThread.path.connect(self.directoryFinder)
    
    def directoryFinder(self, path):
        self.path = path
        print(self.path)
        self.lista.append(str(path))
        
    def finishDirectoryFinder(self):
        self.setEnabled(True)
        self.d.close()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
