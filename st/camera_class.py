import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import datetime
import time

class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        self.count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(0.1)

    def stop(self):
        self.running = False

class Filter():
    def __init__(self, label1, label2, label3, slider1, slider2, slider3):
        # self.filter = filtering
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3
        self.slider1 = slider1
        self.slider2 = slider2
        self.slider3 = slider3

    def set_param(self):
        pass

    def filtering(self):
        pass

    def turnOn(self):
        self.label1.show()
        self.label2.show()
        self.label3.show()
        self.slider1.show()
        self.slider2.show()
        self.slider3.show()

    def turnOff(self):
        self.label1.hide()
        self.label2.hide()
        self.label3.hide()
        self.slider1.hide()
        self.slider2.hide()
        self.slider3.hide()

class Color_Filter(Filter):
    def __init__(self, label1, label2, label3, slider1, slider2, slider3, btnRgb, btnHsv):
        super().__init__(label1, label2, label3, slider1, slider2, slider3)
        self.btnRgb = btnRgb
        self.btnHsv = btnHsv

    def setParam(self):
        value_h = self.slider1.value()
        value_s = self.slider2.value()
        value_v = self.slider3.value()

        return value_h, value_s, value_v
    def btnOn(self):
        self.btnRgb.show()
        self.btnHsv.show()

    def btnOff(self):
        self.btnRgb.hide()
        self.btnHsv.hide()

class HSV_Filter(Color_Filter):
    def __init__(self, label1, label2, label3, slider1, slider2, slider3, btnRgb, btnHsv):
        super().__init__(label1, label2, label3, slider1, slider2, slider3, btnRgb, btnHsv) 

    def setText(self):
        self.label1.setText("H")
        self.label2.setText("S")
        self.label3.setText("V")

    def setParam(self):
        value_h = self.slider1.value()
        value_s = self.slider2.value()
        value_v = self.slider3.value()

        return value_h, value_s, value_v

    def setRange(self):
        self.slider1.setRange(0, 180)
        self.slider2.setRange(-100, 100)
        self.slider3.setRange(-100, 100)  

    def setValue(self):
        self.slider1.setValue(0)
        self.slider2.setValue(0)
        self.slider3.setValue(0)

    def filtering(self, image, vh, vs, vv):
        src_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        h, s, v = cv2.split(src_hsv)
        
        cvt_h = cv2.add(h, vh)
        cvt_s = cv2.add(s, vs)
        cvt_v = cv2.add(v, vv)

        dst_hsv = cv2.merge((cvt_h, cvt_s, cvt_v))
        dst = cv2.cvtColor(dst_hsv, cv2.COLOR_HSV2RGB)

        return dst

class RGB_Filter(Color_Filter):
    def __init__(self, label1, label2, label3, slider1, slider2, slider3, btnRgb, btnHsv):
        super().__init__(label1, label2, label3, slider1, slider2, slider3, btnRgb, btnHsv)  
        
    def setText(self):
        self.label1.setText("R")
        self.label2.setText("G")
        self.label3.setText("B")    

    def setParam(self):
        value_1 = self.slider1.value()
        value_2 = self.slider2.value()
        value_3 = self.slider3.value()

        return value_1, value_2, value_3

    def setRange(self):
        self.slider1.setRange(-100, 100)
        self.slider2.setRange(-100, 100)
        self.slider3.setRange(-100, 100) 

    def setValue(self):
        self.slider1.setValue(0)
        self.slider2.setValue(0)
        self.slider3.setValue(0)

    def filtering(self, image, vr, vg, vb):
        # src_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        r, g, b = cv2.split(image)

        cvt_r = cv2.add(r , vr)
        cvt_g = cv2.add(g , vg)
        cvt_b = cv2.add(b , vb)

        dst = cv2.merge((cvt_r, cvt_g, cvt_b))
        # dst = cv2.cvtColor(dst_rgb, cv2.COLOR_RGB2BGR)

        return dst    

class Alpha(RGB_Filter):
    def __init__(self, label1, label2, label3, slider1, slider2, slider3, label4, slider4, btnRgb, btnHsv):
        super().__init__(label1, label2, label3, slider1, slider2, slider3, btnRgb, btnHsv)
        self.label4 = label4
        self.slider4 = slider4

    def setParam(self):
        super().setParam()
        value = self.slider4.value()

        return value

    def setRange(self):
        super().setRange()
        self.slider4.setRange(0, 100)

    def setValue(self):
        super().setValue()
        self.slider4.setValue(100)

    def setText(self):
        super().setText()
        self.label4.setText("A")

    def tunrOn(self):
        super().turnOn()
        self.label4.show()
        self.slider4.show()

    def tunrOff(self):
        super().turnOff()
        self.label4.hide()
        self.slider4.hide()

from_class = uic.loadUiType("./camera.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.camera = Camera(self)
        self.camera.daemon = True
        self.record = Camera(self)
        self.record.daemon = True

        self.filter = Filter(self.label1, self.label2, self.label3,
                             self.slider1, self.slider2, self.slider3)
        self.color_filter = Color_Filter(self.label1, self.label2, self.label3, self.slider1, self.slider2, self.slider3, self.btnRgb, self.btnHsv)
        self.hsv_filter = HSV_Filter(self.label1, self.label2, self.label3, self.slider1, self.slider2, self.slider3, self.btnRgb, self.btnHsv)
        self.rgb_filter = RGB_Filter(self.label1, self.label2, self.label3, self.slider1, self.slider2, self.slider3, self.btnRgb, self.btnHsv)
        self.alpha_filter = Alpha(self.label1, self.label2, self.label3, self.slider1, self.slider2, self.slider3, self.label4, self.slider4, self.btnRgb, self.btnHsv)

        self.x, self.y = None, None
        self.initUi()

    def initUi(self):
        self.isRecStart = False

        self.labelRecord.hide()
        self.labelRec.hide()
        self.btnRecord.hide()
        self.btnErase.hide()
        self.btnCapture_2.hide()
        self.color_filter.btnOff()
        self.alpha_filter.tunrOff()

        self.pixmap = QPixmap()
        self.width = self.pixmap.width()
        self.height = self.pixmap.height()

        self.pixmap2 = QPixmap(self.label.width(), self.label.height())
        self.label.setPixmap(self.pixmap2)  
        self.btnErase.clicked.connect(self.erase)

        self.camera.update.connect(self.updateCamera)
        self.btnColor.clicked.connect(self.clickColor)

        self.btnPhoto.clicked.connect(self.modeCamera)
        self.btnCapture.clicked.connect(self.capture)
        self.btnCapture_2.clicked.connect(self.capture)

        self.record.update.connect(self.updateRecording)
        self.btnVideo.clicked.connect(self.modeRecord)
        self.btnRecord.clicked.connect(self.clickRecord)

        self.sliderScale.setRange(1,5)
        self.sliderScale.valueChanged.connect(self.scaler)

        self.isDrawOn = False
        self.btnDraw.clicked.connect(self.clickDraw)

        self.per = 0
        self.count = 0
        self.color = None
        self.isColorOn = False
        self.cameraStart()

    def scaler(self):
        scale = self.sliderScale.value()
        self.width = self.width * scale
        self.height = self.height * scale
        
    def clickColor(self):
        if self.isColorOn == False:
            self.color_filter.btnOn()
            self.isColorOn = True
        else:
            self.filter.turnOff()
            self.color_filter.btnOff()
            self.isColorOn = False

        self.btnRgb.clicked.connect(self.clickRgb)
        self.btnHsv.clicked.connect(self.clickHsv)

    def updateColor(self, image):
        value_1, value_2, value_3 = self.color_filter.setParam()
        if self.color == "RGB":
            image = self.rgb_filter.filtering(image, value_1, value_2, value_3)
        elif self.color == "HSV":
            image = self.hsv_filter.filtering(image, value_1, value_2, value_3)
        return image

    def clickRgb(self):
        self.color_filter.btnOff()
        self.rgb_filter.turnOn()
        self.rgb_filter.setText()
        self.rgb_filter.setRange()
        self.rgb_filter.setValue()

    def clickHsv(self):
        self.color_filter.btnOff()
        self.hsv_filter.turnOn()
        self.hsv_filter.setText()   
        self.hsv_filter.setRange()
        self.hsv_filter.setValue()

    def clickDraw(self):
        if self.isDrawOn == False:
            self.isDrawOn = True

            self.alpha_filter.tunrOn()
            self.alpha_filter.setText()
            self.alpha_filter.setRange()
            self.alpha_filter.setValue()

            self.btnErase.show()
            self.btnColor.hide()
            self.btnFilter.hide()

        else:
            self.isDrawOn = False

            self.alpha_filter.tunrOff()

            self.btnErase.hide()
            self.btnColor.show()
            self.btnFilter.show()

    def mouseMoveEvent(self, event):
        if self.isDrawOn == True:
            if self.x is None:
                self.x = event.x()
                self.y = event.y()
                return
            
            value_1, value_2, value_3, value_4 = self.alpha_filter.setParam()

            self.color_rgb = (value_1, value_2, value_3, value_4)
            self.btnDraw.setStyleSheet(
                "background-color: rgb{color}; border-radius: 18px; border-style: outset;" 
                .format(color = self.color_rgb))

            self.update()


            painter = QPainter(self.label.pixmap())
            painter.setPen(QPen(QColor(value_1, value_2, value_3, value_4), 
                                        20, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.x - self.label.x(), self.y - self.label.y(), 
                            event.x() - self.label.x(), event.y() - self.label.y())
            painter.end()
            self.update()

            self.x = event.x()
            self.y = event.y()
        else:
            pass
    def mouseReleaseEvent(self, event):
        if self.isDrawOn == True:
            self.x = None
            self.y = None
        else:
            pass

    def erase(self):
        self.label.setPixmap(self.pixmap2)

    def cameraStart(self):
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(2)

    def updateCamera(self):
        retval, self.image = self.video.read()

        if retval:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            h, w, c = self.image.shape
            image = self.image

            image = self.updateColor(image)
            self.img_cvt = image

            qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.display.width(), self.display.height())

            self.display.setPixmap(self.pixmap)
        
        # self.count += 1

    def capture(self):
        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = './data/' + self.now + '.png'

        cv2.imwrite(filename, cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))

    def modeRecord(self):
        self.btnCapture.hide()
        self.btnRecord.show()

    def modeCamera(self):
        self.btnRecord.hide()
        self.btnCapture.show()
        self.recordingStop()

    def clickRecord(self):
        if self.isRecStart == False:
            self.labelRecord.show()
            self.btnPhoto.hide()
            self.btnVideo.hide()
            self.btnDoc.hide()
            self.btnCapture_2.show()
            self.isRecStart = True
            self.recordingStart()
        else:
            self.labelRecord.hide()
            self.btnPhoto.show()
            self.btnVideo.show()
            self.btnDoc.show()
            self.btnCapture_2.hide()
            self.isRecStart = False
            self.recordingStop()

    def updateRecording(self):
        self.count += 1
        self.writer.write(self.image)
        
        if self.count % 8 == 0:
            self.labelRec.hide()
        else:
            self.labelRec.show()

    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = './data/' + self.now + '.avi'
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w, h))

    def recordingStop(self):
        self.record.running = False
        self.labelRec.hide()

        if self.isRecStart == True:
            self.writer.release()
            self.labelRec.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())