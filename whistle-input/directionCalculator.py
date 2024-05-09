from scipy import signal
import numpy as np
class FreqCalculator():
    def __init__(self,rate):
        self.rate = rate
        self.kernel_size = 21
        self.kernel_sigma = 3
        self.kernel = signal.windows.gaussian(self.kernel_size, self.kernel_sigma)
        self.past_frequencies = []
        self.ascention_threathhold = 10
        self.frequency_compare_num = 6
        self.deleteFrequenciesTime = 1.0
        self.deletionCountDown = self.deleteFrequenciesTime
        self.minimumVolume = 200000
    
    def check_direction(self):
        
        print(len(self.past_frequencies))
        if len(self.past_frequencies) >= self.frequency_compare_num:    

            ascention_counter = 0
            for i in range(len(self.past_frequencies)-2):
                ascention_counter +=  self.past_frequencies[i+1] - self.past_frequencies[i]
            self.past_frequencies.clear()        
            
            if(np.abs(ascention_counter)>self.ascention_threathhold):
                if(ascention_counter>0):
                    #print("up")
                    return "scrole_up"
                else: 
                    #print("down")
                    return "scrole_down"
            
        
        return "scrole_no"
                        
            
        
    
    
    def calculate_main_frequency(self,data):
        self.data = np.frombuffer(data, dtype=np.int16)
        self.data = self.data * np.hamming(len(self.data))
        self.data = np.convolve(self.data, self.kernel, 'same')
        spectrum = np.abs(np.fft.fft(self.data))
        #stronges_frequency=max(spectrum)
        frequencies = np.fft.fftfreq(len(self.data), d=1 / self.rate)
        mask = frequencies >=0
        spectrum_max = np.argmax(spectrum[mask])
        #print(spectrum_max)
        if np.max(spectrum[mask])>self.minimumVolume:
            max_frequency = frequencies[mask][spectrum_max]
            #print("-")
            #print(max_frequency)
            if max_frequency != 0:
                self.past_frequencies.append(max_frequency) 
            return self.check_direction()       
        else: 
            return "scrole_no"
                
    def update(self, data):
        
       result = self.calculate_main_frequency(data)
       #print(result) 
       return result 
                       
                #print(midi_note)
                
                #print(midi_note)
  
        #else:
        #     return None   
        
        #print(np.where(data == stronges_frequency))

        
    def lowerTimer(self,dt):
        if self.past_frequencies:
            del self.past_frequencies[0] #.remove(self.past_frequencies[0])
            #self.deletionCountDown -dt