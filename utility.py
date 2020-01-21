import sys
import test_ui
from PyQt5 import uic
from PyQt5.QtWidgets import *
e = test_ui.Ui_MainWindow()
app = QApplication([])
w = QMainWindow()
layout = QGridLayout()
w.show()
e.setupUi(w)
app.exec_()


if __name__ == "__mkain__":
   Form, Window = uic.loadUiType("test.ui")
   app = QApplication([])
   window = Window()
   form = Form()
   form.setupUi(window)
   window.show()
   app.exec_()