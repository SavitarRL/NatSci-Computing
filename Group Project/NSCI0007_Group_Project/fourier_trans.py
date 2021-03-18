import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import librosa.display

def dominant_freq_extractor(audiofile, k):
    signal, sample_rate = librosa.load(audiofile) #read audiofile
    N = signal.size
    fouriertrans = fft(signal) #fourier transform of the audiosignal 
    power = np.abs(fouriertrans)**2 #power in db is the modulus of the fourier transform ^2 as certain elements in the array are complex
    freq_vector = fftfreq(N, 1 / sample_rate) #create a frequency vector 
    max_indices = (-power).argsort()[:k] #this array contains the indices for k highest values in the power 
    dominant_freqs = abs(freq_vector[max_indices])
    return dominant_freqs

def dominant_freq_extractor_string(audiofile, k):
    signal, sample_rate = librosa.load(audiofile) #Read audiofile
    N = signal.size
    fouriertrans = fft(signal) #Fourier transform of the audiosignal
    power = np.abs(fouriertrans)**2 #Power in db is the modulus of the fourier transform ^2 as certain elements in the array are complex
    freq_vector = fftfreq(N, 1 / sample_rate) #Create a frequency vector
    max_indices = (-power).argsort()[:k] #This array contains the indices for k highest values in the power
    dominant_freqs = np.abs(freq_vector[max_indices])
    for i in range(0,k):
        print("Dominant Frequency",format(i+1),":", dominant_freqs[i])