from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic

from circularprogressbar import QRoundProgressBar
from opcua import Client

import threading , random
from time import sleep

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('OpcuaClient.ui',self)

        self.url = "opc.tcp://111.111.11.11:1111"

        self.tempbar = QRoundProgressBar()
        self.tempbar.setFixedSize(400, 400)
        self.tempbar.setDataPenWidth(3)
        self.tempbar.setOutlinePenWidth(3)
        self.tempbar.setDonutThicknessRatio(0.85)
        self.tempbar.setDecimals(1)
        self.tempbar.setFormat('%v C| %p %')
        self.tempbar.setNullPosition(90)
        self.tempbar.setBarStyle(QRoundProgressBar.StyleDonut)
        self.tempbar.setDataColors([(0., QColor.fromRgb(0,255,0)), (0.5, QColor.fromRgb(255,255,0)), (1., QColor.fromRgb(255,0,0))])

        self.tempbar.setRange(0, 50)
        self.tempbar.setValue(50)
        self.horizontalLayout.addWidget(self.tempbar)

        self.pressbar = QRoundProgressBar()
        self.pressbar.setFixedSize(400, 400)
        self.pressbar.setDataPenWidth(3)
        self.pressbar.setOutlinePenWidth(3)
        self.pressbar.setDonutThicknessRatio(0.85)
        self.pressbar.setDecimals(1)
        self.pressbar.setFormat('%v Pas| %p %')
        self.pressbar.setNullPosition(90)
        self.pressbar.setBarStyle(QRoundProgressBar.StylePie)
        self.pressbar.setDataColors([(0., QColor.fromRgb(0,255,0)), (0.5, QColor.fromRgb(255,255,0)), (1., QColor.fromRgb(255,0,0))])

        self.pressbar.setRange(0, 200)
        self.pressbar.setValue(200)
        self.horizontalLayout_2.addWidget(self.pressbar)

        self.ui.pushBtnStart.clicked.connect(self.startDataTake)
        self.ui.pushBtnStop.clicked.connect(self.stopDataTake)
        self.ui.pushButtonConnect.clicked.connect(self.connectServer)

        self.isRun = False
        self.connect = False

        self.TempSwitch = False
        self.PressSwitch = False

    def connectServer(self):
        self.url = self.ui.lineEditSeverIP.text()
        self.client = Client(self.url)

        try:
            self.client.connect()
        except OSError:
            QMessageBox.warning(self,'Warning',f"Oops! Failed to set the OPC UA endpoint.\nPlease check the IP Address and port. \n{self.url} not valid ")
            print(f"Oops! Failed to set the OPC UA endpoint. Please check the IP Address and port {self.url} not valid ")
            return
        print("Server connected")
        self.ui.labelConnectStatus.setText("Connected")
        self.connect = True

    def startDataTake(self):
        if(self.connect==True):
            self.isRun = True
            for t in threading.enumerate():
                if t.name == "_gen_":
                    print("already running")
                    return
            threading.Thread(target=self.backgroundThread, name="_gen_").start()
            print("clicked Start")
        else:
            QMessageBox.warning(self,'Warning',f"Oops! OPC Server has not been connected\n Please connect it first")

    def stopDataTake(self):
        self.isRun = False
        for t in threading.enumerate():
            if t is self.backgroundThread:
                t.join()
        print("Clicked Stop")

    def disconnectServer(self):
        if(self.connect == True):
            self.client.disconnect()

    def backgroundThread(self):
        TempSwitch = self.client.get_node("ns=2;i=2")
        PressSwitch = self.client.get_node("ns=2;i=3")
        Temp = self.client.get_node("ns=2;i=4")
        Press = self.client.get_node("ns=2;i=5")
        Time = self.client.get_node("ns=2;i=6")
        
        
        while(self.isRun):
            self.TempSwitch = TempSwitch.get_value()
            self.PressSwitch = PressSwitch.get_value()
            self.tempValue = Temp.get_value()
            self.pressValue = Press.get_value()
            self.Time = Time.get_value()

            if (self.TempSwitch == True):
                self.ui.labelTemp.setText("ON")
                self.tempbar.setValue(self.tempValue)
            else:
                self.ui.labelTemp.setText("OFF")
                self.tempbar.setValue(0)

            if (self.PressSwitch == True):
                self.ui.labelPress.setText("ON")
                self.pressbar.setValue(self.pressValue)
            else:
                self.ui.labelPress.setText("OFF")
                self.pressbar.setValue(0)
            self.ui.labelTimeDate.setText(str(self.Time))
            sleep(0.1)
