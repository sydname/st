import sys
import cv2
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import mysql.connector
import datetime
import time
import serial
import threading
import time
import numpy as np

# py_serial = serial.Serial("/dev/ttyACM0", 9600)
# read = True
# datos = ""
# serial_reads = ["start serial"]


class Time(QThread):
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        self.count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(2)

    def stop(self):
        self.running = False

form_class = uic.loadUiType("GUI.ui")[0]
form_cam_Class = uic.loadUiType("Cam.ui")[0]

class WindowClass(QMainWindow, form_class):  # GUI 클래스
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.setIcon()
        self.connectSql()
        self.pulseData = self.fetchPulse()

        # self.time = Time(self)
        # self.time.daemon = True
        # self.time.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.timeout.connect(self.fetchPulse)
        self.timer.start(1000) # 1000ms = 1s

        self.updateTime()
        
    def initUI(self):
        self.btnCameraPage.clicked.connect(self.cameraPage)
        self.btnSetting.clicked.connect(self.settingPage)
        self.btnGpsPage.clicked.connect(self.gpsPage)
        self.btnPlayPage.clicked.connect(self.playPage)

        self.btnFeed.clicked.connect(self.feeding)

        self.labelFood.hide()

    def connectSql(self):
        self.local = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "0050",
            database = "test_aruino"
        )

    def fetchPulse(self):
        self.cur = self.local.cursor(buffered=True)
        self.cur.execute("SELECT * FROM pulse order by rand() limit 1") 
        # self.cur.execute("select pulse from pulse order by date_timestamp desc limit 1")
        self.pulseData = self.cur.fetchall()
        self.labelPulse.setText(str(self.pulseData[0][0]))

    def updateTime(self):
        self.now = datetime.datetime.now().strftime('%Y년 %m월 %d일  %H : %M : %S  ')
        self.labelDateTime.setText(self.now)

    def setIcon(self):
        self.btnCameraPage.setIcon(QIcon("../icon/webcam.png"))
        self.btnCameraPage.setIconSize(QSize(50, 50))
        self.btnPlayPage.setIcon(QIcon("../icon/ball.png"))
        self.btnPlayPage.setIconSize(QSize(50, 50))
        self.btnGpsPage.setFont(QFont("ubuntu", 25, weight=QFont.Bold))
        self.btnGpsPage.setText("GPS")
        self.btnSetting.setIcon(QIcon("../icon/setting.png"))
        # self.btnSetting.setStyleSheet("background-color: transparent;")

        self.labelDog.setPixmap(QPixmap("../icon/dog-sit.png"))
        self.labelDog.setStyleSheet("background-color: transparent;")

        self.btnFeed.setIcon(QIcon("../icon/pet-food.png"))
        self.btnHeart.setIcon(QIcon("../icon/heart.png"))

        self.labelFood.setPixmap(QPixmap("../icon/pet-food-filling.png"))
        self.labelFoodEmpty.setPixmap(QPixmap("../icon/pet-bowl.png"))
        self.labelWater.setPixmap(QPixmap("../icon/water-bowl.png"))
        
        self.labelPulseIcon.setPixmap(QPixmap("../icon/pulse.png"))
        self.labelPawIcon.setPixmap(QPixmap("../icon/paws.png"))
        self.labelPawIcon2.setPixmap(QPixmap("../icon/paws.png"))

    def feeding(self):
        self.labelFoodEmpty.hide()
        self.labelFood.show()

    def cameraPage(self):
        self.hide()
        self.cam = CamWindowClass(self)
        # self.cam.exec()
        self.cam.show()

    def gpsPage(self):
        pass

    def playPage(self):
        pass

    def settingPage(self):
        pass

class CamWindowClass(QMainWindow, form_cam_Class):
    def __init__(self, windowClass):
        # super(CamWindowClass, self).__init__() # why CamWindowClass?
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.setIcon()

        self.windowClass = windowClass

        # print("windowClass set in CamWindowClass", self.windowClass)

    def initUI(self):
        self.btnMainPage.clicked.connect(self.mainPage)
        self.btnRight.clicked.connect(lambda : self.cameraMove("right"))
        self.btnDown.clicked.connect(lambda : self.cameraMove("down"))
        self.btnUp.clicked.connect(lambda : self.cameraMove("up"))
        self.btnLeft.clicked.connect(lambda : self.cameraMove("left"))

        # self.labelPulse.setText(str(self.windowClass.labelPulse.text()))

        # if hasattr(self.windowClass, 'labelPulse'):
        #     self.labelPulse.setText(str(self.windowClass.labelPulse.text()))
        # else:
        #     print("Error : windowClass does not have 'labelPulse' attribute")

        self.btnGood.clicked.connect(lambda : self.sendSound("good"))
        self.btnComeOn.clicked.connect(lambda : self.sendSound("comeon"))


    def setIcon(self):
        self.btnMainPage.setIcon(QIcon("../icon/home.png"))
        self.btnRight.setIcon(QIcon("../icon/arrow-right.png"))
        self.btnDown.setIcon(QIcon("../icon/arrow-down.png"))
        self.btnUp.setIcon(QIcon("../icon/right-arrow.png"))
        self.btnLeft.setIcon(QIcon("../icon/play.png"))
        self.btnFeed.setIcon(QIcon("../icon/pet-food.png"))
        self.btnPlay.setIcon(QIcon("../icon/ball.png"))
               
        self.labelPulseIcon.setPixmap(QPixmap("../icon/pulse.png"))
    
    def sendSound(self, key):
        self.sound = QSoundEffect()
        match(key):
            case "good":
                self.sound.setSource(QUrl.fromLocalFile("../data/dog-barking-twice.wav"))
            case "comeon":
                self.sound.setSource(QUrl.fromLocalFile("../data/meow.wav"))
        self.sound.play()

    def cameraMove(self, key):
        x = self.label.x()
        y = self.label.y()

        match(key):
            case "right":
                x += 10
            case "left":
                x -= 10
            case "up":
                y -= 10
            case "down":
                y += 10

        self.label.move(x, y)

    def mainPage(self):
        self.hide()
        self.main = WindowClass()
        # self.main.exec()
        self.main.show()

# app = QApplication(sys.argv)
# myWindows = WindowClass()
# def sendSerial(key=0, message=""):
#         output = f"{key:02}" + message
#         py_serial.write(output.encode())
#         time.sleep(0.1)
# def receiveSerialEvent():
#     global py_serial, read, datos, serial_reads, myWindows
#     while read is True:
#         datos = py_serial.read_until().decode('ascii').strip()
#         serial_reads.append(datos)
#         if datos == "end serial":
#             print("Serial Read!!")
#             print(serial_reads)
#             myWindows.labelPulse.setText(serial_reads[1])
#             serial_reads = ["start serial"]
#     return
# t = threading.Thread(target=receiveSerialEvent)
# t.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)   
    myWindows = WindowClass()   

    myWindows.show()
    sys.exit(app.exec_())