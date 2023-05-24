from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from loadGui import MainApp

class MyWidget(MainApp):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #self.setupUi(self)
     
    def closeEvent(self, event):
        reply = QMessageBox.question(self,'Window Close', 'Are you sure you want to close the window',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
            MainApp.stopDataTake(self)
            MainApp.disconnectServer(self)
            print("Window Close")
        else:
            event.ignore()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myWidget = MyWidget()
    
    myWidget.show()
    #myWidget.showFullScreen()
    sys.exit(app.exec())