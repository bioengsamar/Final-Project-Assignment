import numpy as np
import librosa

class AudioModel():
    def __init__(self, audioPath: str):        
        self.y, self.sr = librosa.load(audioPath)
        S_full, phase = librosa.magphase(librosa.stft(self.y))
        S_filter = librosa.decompose.nn_filter(S_full,
                                            aggregate=np.median,
                                            metric='cosine',
                                            width=int(librosa.time_to_frames(2, sr=self.sr)))
        S_filter = np.minimum(S_full, S_filter)
        margin_i, margin_v = 2, 10
        power = 2
        mask_i = librosa.util.softmask(S_filter,
                                    margin_i * (S_full - S_filter),
                                    power=power)
        mask_v = librosa.util.softmask(S_full - S_filter,
                                    margin_v * S_filter,
                                    power=power)
        S_foreground = mask_v * S_full
        S_background = mask_i * S_full
        self.vocals = librosa.istft(S_foreground*phase)
        self.music = librosa.istft(S_background*phase)
        # librosa.output.write_wav("result/songAnalysis/vocals.wav", self.vocals, self.sr)
        # librosa.output.write_wav("result/songAnalysis/music.wav", self.music, self.sr)