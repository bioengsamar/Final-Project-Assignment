from PyQt5 import QtWidgets, QtGui, QtCore
from SuperStarGUI import Ui_MainWindow
import sys
import numpy as np
import sounddevice as sd

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.gsample = [i for i in range(6)]
        self.butns_guitar=[self.ui.th_1,self.ui.th_2,self.ui.th_3,
                           self.ui.th_4,self.ui.th_5,self.ui.th_6]
        self.funcs_guitar=[lambda:self.guitar(0),lambda:self.guitar(1),lambda:self.guitar(2),
                           lambda:self.guitar(3),lambda:self.guitar(4),lambda:self.guitar(5)]
        for i in range(6):
            self.butns_guitar[i].clicked.connect(self.funcs_guitar[i])
        self.guitar_sounds()
        self.butns_piano=[self.ui.bt_1,self.ui.bt_2,self.ui.bt_3,self.ui.bt_4,self.ui.bt_5,self.ui.bt_6,
                          self.ui.bt_7,self.ui.bt_8,self.ui.bt_9,self.ui.bt_10,self.ui.bt_11,self.ui.bt_12,
                          self.ui.bt_13,self.ui.bt_14,self.ui.bt_15,self.ui.bt_16,self.ui.bt_17,self.ui.bt_18,
                          self.ui.bt_19,self.ui.bt_20,self.ui.bt_21,self.ui.bt_22,self.ui.bt_23,self.ui.bt_24,
                          self.ui.bt_25]
        self.funcs_piano=[lambda:self.piano(0),lambda:self.piano(1),lambda:self.piano(2),
                           lambda:self.piano(3),lambda:self.piano(4),lambda:self.piano(5),
                           lambda:self.piano(6),lambda:self.piano(7),lambda:self.piano(8),
                           lambda:self.piano(9),lambda:self.piano(10),lambda:self.piano(11),
                           lambda:self.piano(12),lambda:self.piano(13),lambda:self.piano(14),
                           lambda:self.piano(15),lambda:self.piano(16),lambda:self.piano(17),
                           lambda:self.piano(18),lambda:self.piano(19),lambda:self.piano(20),
                           lambda:self.piano(21),lambda:self.piano(22),lambda:self.piano(23),
                           lambda:self.piano(24)]
        for i in range(25):
            self.butns_piano[i-1].clicked.connect(self.funcs_piano[i-1])

#### GUITAR Implementation ####    
    def guitar_sounds(self):
        fs = 80000
        freqs = [98, 123, 147, 196, 294, 392]
        for i in range(6):
            wavetable_size = fs // freqs[i] 
            wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
            self.gsample[i] = self.karplus_strong(wavetable,  3*fs)

    def karplus_strong(self,wavetable, n_samples):
        samples = []
        current_sample = 0
        previous_value = 0
        while len(samples) < n_samples:
            wavetable[current_sample] = 0.5 * (wavetable[current_sample] + previous_value)
            samples.append(wavetable[current_sample])
            previous_value = samples[-1]
            current_sample += 1
            current_sample = current_sample % wavetable.size
        return np.array(samples)
    
    def guitar(self,i):
        sd.play(self.gsample[i], 80000)   

#### PIANO Implementation ####        
    def sounds_piano(self,frequency):
        global fs
        fs=8000
        time = np.linspace(0, 1, num=fs)
        Y = np.sin(2 * np.pi * frequency * time) * np.exp(-0.0015 * 2 * np.pi * frequency * time)
        Y += np.sin(2 * 2 * np.pi * frequency * time) * np.exp(-0.0015 * 2 * np.pi * frequency * time) / 2
        Y += np.sin(3 * 2 * np.pi * frequency * time) * np.exp(-0.0015 * 2 * np.pi * frequency * time) / 4
        Y += np.sin(4 * 2 * np.pi * frequency * time) * np.exp(-0.0015 * 2 * np.pi * frequency * time) / 8
        Y += np.sin(5 * 2 * np.pi * frequency * time) * np.exp(-0.0015 * 2 * np.pi * frequency * time) / 16
        Y += np.sin(6 * 2 * np.pi * frequency * time) * np.exp(-0.0015 * 2 * np.pi * frequency * time) / 32
        Y += Y * Y * Y
        Y *= 1 + 16 * time * np.exp(-6 * time)
        return Y
    def piano(self,i):
        frequency=[261.63,277.18,293.66,311.13,329.63,349.23,369.99,392.00,415.30,440.00,466.16,
                   493.88,523.25,554.37,587.33,622.25,659.25,698.46,739.99,783.99,830.61,880.00,
                   932.33,987.77,1046.50]
        sample=self.sounds_piano(frequency[i])
        sd.play(sample,8000)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()