from PyQt5 import QtWidgets, QtGui
from jpeg import Ui_MainWindow
from turbojpeg_offline import TurboJPEG
import sys


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.radioButton_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.radioButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.radioButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        ui = self.ui
        self.images = [ui.img1_1, ui.img1_2, ui.img1_3, ui.img1_4, ui.img1_5, ui.img1_6, ui.img1_7, ui.img1_8,
                       ui.img1_9, ui.img1_10, ui.img1_11, ui.img1_12, ui.img1_13, ui.img1_14, ui.img1_15, ui.img1_16,
                       ui.img1_17, ui.img1_18, ui.img1_19, ui.img1_20, ui.img1_21, ui.img1_22, ui.img1_23, ui.img1_24]
    def im(self,bath,i):
        jpeg=TurboJPEG()
        in_file = open(bath, 'rb')
        img_array = jpeg.decode(in_file.read(),i)            
        return img_array
            
    def load_image(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', 'sources', 'Image Files (*.jpg *.jpeg)')[0]
        if path:
            self.ui.textCurrentFile.setText(path)
            self.ui.radioButton_1.setEnabled(True)
            self.ui.radioButton_2.setEnabled(True)
            self.ui.radioButton_3.setEnabled(True)
            for i in range(8):
                i_ = -i + 8
                img=QtGui.QImage(self.im(path,i_),self.im(path,i_).shape[1],self.im(path,i_).shape[0],QtGui.QImage.Format_RGB888)
                self.images[i].setPixmap(QtGui.QPixmap(img))
                self.images[i+8].setPixmap(QtGui.QPixmap(img))
                self.images[i+16].setPixmap(QtGui.QPixmap(img))
        else:
            self.ui.textCurrentFile.setText("You didn't choose any file!")

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()