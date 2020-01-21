import PyQt5


from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox


class BSCPS_GUI():

    def on_button_clicked(self):
        pass


    def __init__(self):
        self.app = QApplication([])
        self.Mwindow = QMainWindow()


        self.window = QWidget(self.Mwindow)
        self.window.setObjectName("centralwidget")
        layout = QGridLayout()
        buttonlayout = QHBoxLayout()
        layout.addChildLayout(buttonlayout)

        self.b1 = QPushButton("Sort By Rating")
        self.b2 = QPushButton("Sort By Tag(s)")

        self.b1.clicked.connect(self.on_button_clicked)


        buttonlayout.addWidget(self.b1)
        buttonlayout.addWidget(self.b2)
        buttonlayout.addWidget(QPushButton("Two"), )


        #layout.addWidget(QLabel('yeet'))

        self.Mwindow.show()
        self.app.exec_()




if __name__ =='__main__':
    app = BSCPS_GUI()
    #app.app.exec_()