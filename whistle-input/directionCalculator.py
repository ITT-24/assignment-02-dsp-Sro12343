from scipy import signal
import numpy as np
class DirCalculator():
    def __init__(self,rate):
        # Initialize instance variables 
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
        # Check if enough frequnecies measured for input        
        if len(self.past_frequencies) >= self.frequency_compare_num:    
            #start with nutral direction
            ascention_counter = 0
            #for every possible frequency check if the next frequency is smaler or biger and add it to the direction
            for i in range(len(self.past_frequencies)-2):
                ascention_counter +=  self.past_frequencies[i+1] - self.past_frequencies[i]
            #empty the measuered frequency to be ready for next input
            self.past_frequencies.clear()        
            
            #check if the difference was enough to make input
            if(np.abs(ascention_counter)>self.ascention_threathhold):
                if(ascention_counter>0):
                    return "scroll_up"
                else: 
                    return "scroll_down"        
        return "scroll_no"
    
    def calculate_main_frequency(self,data):
        #convert to array
        self.data = np.frombuffer(data, dtype=np.int16)
        #hamming the input
        self.data = self.data * np.hamming(len(self.data))
        #mitigate background noise 
        self.data = np.convolve(self.data, self.kernel, 'same')
        # Perform Fourier transform to obtain the spectrum
        spectrum = np.abs(np.fft.fft(self.data))
        # Compute frequencies corresponding to each spectrum component
        frequencies = np.fft.fftfreq(len(self.data), d=1 / self.rate)
        # Create a mask for positive frequencies
        mask = frequencies >=0
        # Find the index of the maximum value in the spectrum
        spectrum_max = np.argmax(spectrum[mask])
        #check if is loud enough
        if np.max(spectrum[mask])>self.minimumVolume:
            # Retrieve the frequency corresponding to the maximum spectrum value
            max_frequency = frequencies[mask][spectrum_max]
            # Check if the maximum frequency is non-zero
            if max_frequency != 0:
                #add frequency to list of measured frequencies for input measuring
                self.past_frequencies.append(max_frequency) 
            #Check direction input
            return self.check_direction()       
        else: 
            return "scroll_no"
                
    def update(self, data): 
       result = self.calculate_main_frequency(data) 
       return result 
           
    def lowerTimer(self,dt):
        #if list of measured frequencies is not empty, delete the oldest input.
        #This deletes, for example, old irrelevant frequencies
        #It allows concrete input attempts.
        if self.past_frequencies:
            del self.past_frequencies[0]