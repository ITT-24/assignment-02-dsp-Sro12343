from scipy import signal
import numpy as np
class FreqCalculator():
    def __init__(self,rate):
        self.rate = rate
        self.kernel_size = 21
        self.kernel_sigma = 3
        self.minimum_volume = 90000
        self.kernel = signal.windows.gaussian(self.kernel_size, self.kernel_sigma)
    
    def update(self, data):
        #convert to array
        self.data = np.frombuffer(data, dtype=np.int16)
        #hamming the input
        self.data = self.data * np.hamming(len(self.data))
        #mitigate background noise 
        self.data = np.convolve(self.data, self.kernel, 'same')

        #___
        spectrum = np.abs(np.fft.fft(self.data))
        frequencies = np.fft.fftfreq(len(self.data), d=1 / self.rate)
        mask = frequencies >=0
        spectrum_max = np.argmax(spectrum[mask])

        
        #check if is loud enough
        if np.max(spectrum[mask])>self.minimum_volume:
            max_frequency = frequencies[mask][spectrum_max]
            if max_frequency != 0:
                
                #convert to midi note. Based on ChatGPT: with python i have frequency. how can i convert it into a midi note?
                midi_note = 69 + 12 * np.log2(max_frequency / 440)
                
                #make all octaves the same
                midi_note = midi_note %12 
                
                return midi_note

        return None
        