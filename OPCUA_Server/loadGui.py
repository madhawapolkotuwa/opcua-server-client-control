from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QColor
from PyQt5 import uic
from opcua import Server

import threading , random
import datetime
from time import sleep

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('OpcuaServer.ui',self)

        self.server = Server()
        self.url = "opc.tcp://111.111.1.11:1111"
        self.temp = False
        self.pres = False
        self.connect = False

        self.ui.pushButtonConnect.clicked.connect(self.startServer)
        self.ui.pushButtonTemp.clicked.connect(self.onTemp)
        self.ui.pushButtonPres.clicked.connect(self.onPres)

        self.tempVal = random.randint(10,50)
        self.pressVal = random.randint(100,200)
        
        
    def startServer(self):
        self.temp = True
        self.pres = True
        

        self.url = self.ui.lineEditIpAddress.text()
        print(self.url)
        self.server.set_endpoint(self.url)

        name = "OPCUA_SIMULATION_SEVER"
        addspace = self.server.register_namespace(name)

        node = self.server.get_objects_node()
        Param = node.add_object(addspace,"Parameters")

        self.TempSwitch = Param.add_variable(addspace,"TempSwitch",False)
        self.PressSwitch = Param.add_variable(addspace,"PressSwitch",False)
        self.TempValue = Param.add_variable(addspace,"Temperature",0)
        self.PressValue = Param.add_variable(addspace,"Pressure",0)
        self.Time = Param.add_variable(addspace, "Time",0)

        self.TempValue.set_writable()
        self.PressValue.set_writable()
        self.Time.set_writable()

        #sleep(0.5)
        
        try:
            self.server.start()
        except OSError:
            QMessageBox.warning(self,'Warning',f"Oops! Failed to set the OPC UA endpoint.\nPlease check the IP Address and port. \n{self.url} not valid ")
            print(f"Oops! Failed to set the OPC UA endpoint. Please check the IP Address and port {self.url} not valid ")
            return
        
        self.connect = True
        self.onTemp()
        self.onPres()
        self.startTempThread()

    def stopServer(self):
        if(self.connect==True):
            self.server.stop()

    def startTempThread(self):
        self.isRun = True
        for i in threading.enumerate():
            if i.name == "_temp_":
                print("already running")
                return
        threading.Thread(target=self.backgroundTempThread, name="_temp_").start()  
        print("clicked Start")
    
    def backgroundThreadStop(self):
        self.isRun = False
        for t in threading.enumerate():
            if t is self.backgroundTempThread:
                t.join()
        print("Clicked Stop")

    def  backgroundTempThread(self):
        while ((self.isRun and self.connect)):
            TIME = datetime.datetime.now()
            if(self.temp == True):
                self.tempVal = random.randint(10,50)
                self.TempValue.set_value(self.tempVal)
                #self.pressVal = random.randint(100,200)
                self.ui.labelTempValue.setText(f"{self.tempVal}")
            if(self.pres == True):
                self.pressVal = random.randint(100,200)
                self.PressValue.set_value(self.pressVal)
                self.ui.labelPresValue.setText(f"{self.pressVal}")

            #print(f"{self.tempVal}",f"{self.pressVal}")
            #
            self.Time.set_value(TIME)
            sleep(1)
            

    def onTemp(self):
        if (self.temp != True):
            self.ui.labelTemp.setText("ON")
            self.temp = True
            self.TempSwitch.set_value(True)
        else:
            self.ui.labelTemp.setText("OFF")
            self.temp = False
            self.TempSwitch.set_value(False)
        
    def onPres(self):
        if (self.pres != True):
            self.ui.labelPres.setText("ON")
            self.pres = True
            self.PressSwitch.set_value(True)
        else:
            self.ui.labelPres.setText("OFF")
            self.pres = False
            self.PressSwitch.set_value(False)



