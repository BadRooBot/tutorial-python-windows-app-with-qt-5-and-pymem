from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import psutil
from pymem import *
from pymem.process import *
import test_app_rc

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(449, 411)
        MainWindow.setMaximumSize(QSize(449, 411))
        MainWindow.setStyleSheet(u"")
        self.btn_start = QAction(MainWindow)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_stop = QAction(MainWindow)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_exit = QAction(MainWindow)
        self.btn_exit.setObjectName(u"btn_exit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.lbl_name = QLabel(self.centralwidget)
        self.lbl_name.setObjectName(u"lbl_name")
        self.lbl_name.setGeometry(QRect(0, 0, 450, 50))
        font = QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_name.setFont(font)
        self.lbl_name.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(37, 51, 65);")
        self.lbl_name.setAlignment(Qt.AlignCenter)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 449, 411))
        self.frame.setStyleSheet(u"border-image: url(:/images/Pictures/_49b400d9-1e55-4c4f-a8e1-e9f90cf2c76e.jpg);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        MainWindow.setCentralWidget(self.centralwidget)
        self.frame.raise_()
        self.lbl_name.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 449, 21))
        self.menubar.setStyleSheet(u"background-color: rgb(80, 128, 152);\n"
"color: rgb(255, 255, 255);")
        self.menuStart = QMenu(self.menubar)
        self.menuStart.setObjectName(u"menuStart")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuStart.menuAction())
        self.menuStart.addAction(self.btn_start)
        self.menuStart.addAction(self.btn_stop)
        self.menuStart.addAction(self.btn_exit)
        
        self.retranslateUi(MainWindow)
        
        self.btn_exit.triggered.connect(lambda:self.Exit())
        self.btn_stop.triggered.connect(lambda:self.Stop())
        self.btn_start.triggered.connect(lambda:self.Start("King"))
        
        self.conquerProcess=[]
        self.moudleList=[]
        self.handlerList=[]

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Black lotus test", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"Start ", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.lbl_name.setText(QCoreApplication.translate("MainWindow", u"Black lotus", None))
        self.menuStart.setTitle(QCoreApplication.translate("MainWindow", u"Start", None))
    # retranslateUi
    
    def Exit(self):
        self.close()
        sys.exit()
    
    def Start(self,name):
        self.lbl_name.setText(name)
        print('start')
        self.getAllConquerProc()
    def Stop(self):
        print('stop')
        self.lbl_name.setText('Black lotus')
    
    def getAllConquerProc(self):
        processList=[p.info for p in psutil.process_iter(['name','pid']) ]
        self.conquerProcess=[p for p in processList if p['name'].lower()=='conquer.exe']
        for i in range(len(self.conquerProcess)):
            id=self.conquerProcess[i]['pid']
            name=self.conquerProcess[i]['name']
            handel=Pymem(id)
            module=module_from_name(handel.process_handle,name).lpBaseOfDll
            self.handlerList.append(handel)
            self.moudleList.append(module)
        self.lbl_name.setText(f'{self.conquerProcess}')    
            # handel.write_int(module+0x143fed,2)#with out pointer
            # handel.write_int(self.getAddrOneOrMorePointer(handel,module+0x143fed,[0x3A0]),2)#with  pointer
            
    def getAddrOneOrMorePointer(self,handel,basseAddr,pointr):
        _addr=handel.read_int(basseAddr)
        for offset in pointr:
            if offset != pointr[-1]:
                _addr=handel.read_int(_addr+offset)
            _addr=_addr+offset[-1]
        return _addr            
                    
        
        
        
        
                
            
        
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window=Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())    

