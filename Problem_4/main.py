from PyQt5 import QtWidgets
from GUI import Ui_MainWindow
import sys
from pyqtgraph import mkPen
import sounddevice as sd

import songAnalysis
import coctailAnalysis
import signalAnalysis

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.currentRadio = 5
        self.paths = [None, None, None, None, None]
        self.ui.stackedHome.setCurrentIndex(0)
        self.ui.stackedCoctail.setCurrentIndex(0)
        self.ui.btnHome_1.clicked.connect(lambda: self.ui.stackedHome.setCurrentIndex(0))
        self.ui.btnHome_2.clicked.connect(lambda: self.ui.stackedHome.setCurrentIndex(0))
        self.ui.btnHomeSound.clicked.connect(lambda: self.ui.stackedHome.setCurrentIndex(1))
        self.ui.btnHomeSignal.clicked.connect(lambda: self.ui.stackedHome.setCurrentIndex(2))
        self.ui.btnBackMixer.clicked.connect(lambda: self.ui.stackedCoctail.setCurrentIndex(0))
        self.ui.btnStop.clicked.connect(lambda: sd.stop())
        self.ui.btnMix.clicked.connect(self.mix)
        self.ui.checkBox.hide()
        self.plots = [self.ui.plotMixA, self.ui.plotMixB, self.ui.plotMixC, self.ui.plotMixD, self.ui.plotMixE,
                      self.ui.plotSeparateA, self.ui.plotSeparateB, self.ui.plotSeparateC, self.ui.plotSeparateD, self.ui.plotSeparateE]
        uploaders = [self.ui.btnImportSong, self.ui.btnImportA, self.ui.btnImportB, self.ui.btnImportC, self.ui.btnImportD, self.ui.btnImportE, self.ui.btnImportSignal]
        uploaders_function = [lambda: self.uploader(0), lambda: self.uploader(1), lambda: self.uploader(2), lambda: self.uploader(3), lambda: self.uploader(4), lambda: self.uploader(5), lambda: self.uploader(6)]
        self.uploaders_text = [self.ui.textCurrentFile, self.ui.textCurrentFileA, self.ui.textCurrentFileB, self.ui.textCurrentFileC, self.ui.textCurrentFileD, self.ui.textCurrentFileE, self.ui.textCurrentSingal]
        for i in range(len(uploaders)):
            uploaders[i].clicked.connect(uploaders_function[i])
        radios = [self.ui.radioTwo, self.ui.radioThree, self.ui.radioFour, self.ui.radioFive]
        radios_function = [lambda: self.checkRadios(2), lambda: self.checkRadios(3), lambda: self.checkRadios(4), lambda: self.checkRadios(5)]
        for i in range(len(radios)):
            radios[i].clicked.connect(radios_function[i])
        players = [self.ui.btnPlayMixA, self.ui.btnPlayMixB, self.ui.btnPlayMixC, self.ui.btnPlayMixD, self.ui.btnPlayMixE,
                    self.ui.btnPlaySeparateA, self.ui.btnPlaySeparateB, self.ui.btnPlaySeparateC, self.ui.btnPlaySeparateD, self.ui.btnPlaySeparateE,
                    self.ui.btnPlay, self.ui.btnPlayVocals, self.ui.btnPlayMusic]
        players_function = [lambda: self.player(0), lambda: self.player(1), lambda: self.player(2), lambda: self.player(3), lambda: self.player(4), lambda: self.player(5), lambda: self.player(6), lambda: self.player(7), lambda: self.player(8), lambda: self.player(9), lambda: self.player(10), lambda: self.player(11), lambda: self.player(12)]
        for i in range(len(players)):
            players[i].clicked.connect(players_function[i])
        scalers = [self.ui.btnSignalScaleUp, self.ui.btnSignalScaleDown, self.ui.btnSignalLeft, self.ui.btnSignalRight]
        scalers_function = [lambda: self.scaler(0), lambda: self.scaler(1), lambda: self.scaler(2), lambda: self.scaler(3)]
        for i in range(len(scalers)):
            scalers[i].clicked.connect(scalers_function[i])
    def scaler(self, btnID):
        if btnID == 0:
            self.ui.plotOriginal.getViewBox().scaleBy(x = 0.5, y = 0)
            self.ui.plotSeparate.getViewBox().scaleBy(x = 0.5, y = 0)
        elif btnID == 1:
            self.ui.plotOriginal.getViewBox().scaleBy(x = 2, y = 0)
            self.ui.plotSeparate.getViewBox().scaleBy(x = 2, y = 0)
        elif btnID == 2:
            self.ui.plotOriginal.getViewBox().translateBy(x = -100)
            self.ui.plotSeparate.getViewBox().translateBy(x = -100)
        else:
            self.ui.plotOriginal.getViewBox().translateBy(x = 100)
            self.ui.plotSeparate.getViewBox().translateBy(x = 100)
    def checkRadios(self, sources):
        self.currentRadio = sources
    def uploader(self, btnID):
        if btnID == 0:
            fileType = "MP3 Audio (*.mp3)"
            init = 'songs'
            i = 1
        elif btnID > 0 and btnID <= 5:
            fileType = "Waveform Audio (*.wav)"
            init = 'sources'
            i = 1
        else:
            fileType = "Data File (*.csv)"
            init = 'signals'
            i = 2
        self.ui.stackedHome.setCurrentIndex(3)
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Import Audio", init, fileType)
        if path:
            self.uploaders_text[btnID].setText(path)
            if btnID == 0:
                self.ui.plotSongVocals.getViewBox().clear()
                self.ui.plotSongMusic.getViewBox().clear()
                self.ui.checkBox.setChecked(True)
                self.song = songAnalysis.AudioModel(path)
                self.ui.plotSongVocals.plot(self.song.vocals)
                self.ui.plotSongMusic.plot(self.song.music)
            elif btnID > 0 and btnID <= 5:
                self.uploaders_text[btnID].setEnabled(True)
                self.paths[btnID - 1] = path
            else:
                self.ui.plotOriginal.getViewBox().clear()
                self.ui.plotSeparate.getViewBox().clear()
                self.ui.btnSignalScaleDown.setEnabled(True)
                self.ui.btnSignalScaleUp.setEnabled(True)
                self.ui.btnSignalLeft.setEnabled(True)
                self.ui.btnSignalRight.setEnabled(True)
                self.uploaders_text[btnID].setEnabled(True)
                signal = signalAnalysis.SignalModel(path)
                plots = [self.ui.plotOriginal, self.ui.plotSeparate]
                models = [signal.mix, signal.separate]
                names = ['Mixed Signal','ICA Recovered Signals']
                colors = [mkPen(color=(255, 100, 100)), mkPen(color=(100, 100, 255))]
                for ii, (model, name) in enumerate(zip(models, names), 1):
                    plots[ii-1].setLabel('top', name)
                    for sig, color in zip(model.T, colors):
                        plots[ii-1].plot(sig, pen=color)
        else:
            self.uploaders_text[btnID].setText("You didn't choose any file!")
        self.ui.stackedHome.setCurrentIndex(i)
    def mix(self):
        mix = False
        self.ui.stackedHome.setCurrentIndex(3)
        for i in range(self.currentRadio):
            if self.paths[i] == None:
               self.errorText(i + 1)
               mix = False
            else:
                mix = True
        if mix:
            self.coctail = coctailAnalysis.AudioModel(self.paths, self.currentRadio)
            for i in range(self.currentRadio):
                self.plots[i].getViewBox().clear()
                self.plots[i].plot(self.coctail.mixList[i])
                self.plots[i].setYRange(-30000,30000)
                self.plots[i+5].getViewBox().clear()
                self.plots[i+5].plot(self.coctail.resultList[i])
            self.ui.stackedCoctail.setCurrentIndex(1)
        else:
            pass
        self.ui.stackedHome.setCurrentIndex(1)
    def errorText(self, txtID):
        self.uploaders_text[txtID].setText("You must import source {} to start mixing!".format(txtID))
    def player(self, btnID):
        if btnID >= 5 and btnID < 10:
            data = self.coctail.resultList
            btnID = btnID - 5
            sd.play(data[btnID], 44100)
        elif btnID == 10:
            data = self.song.y
            sd.play(data, self.song.sr)
        elif btnID == 11:
            data = self.song.vocals
            sd.play(data, self.song.sr)
        elif btnID == 12:
            data = self.song.music
            sd.play(data, self.song.sr)
        else:
            data = self.coctail.mixList
            sd.play(data[btnID], 44100)

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()

if __name__ == "__main__":
    main()