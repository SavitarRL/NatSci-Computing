import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import librosa.display
from pydub import AudioSegment
import soundfile
import csv

# Source code: https://stackoverflow.com/questions/60105626/split-audio-on-timestamps-librosa

def closest_species(audiofile):
# Reading the audio file
    dom_f = []
    time = []
    audio, sr = librosa.load(audiofile)
# Splitting the audio files into 0.1 second sections
    buffer = 0.1 * sr

    samples_total = len(audio)
    samples_wrote = 0
    counter = 1
# Carrying out the fourier transform on the whole audio file
    N = len(audio)
    fourier = np.abs(fft(audio))
    freqs = fftfreq(N, 1 / sr)
    maximum = np.argmax(fourier)
    dom = freqs[maximum]

    while samples_wrote < samples_total:
        if buffer > (samples_total - samples_wrote):
            buffer = samples_total - samples_wrote

        block = audio[int(samples_wrote) : int((samples_wrote + buffer))]
# Carrying out the fourier transfrom on each 0.1 second section
        N = len(block)
        yf = np.abs(fft(block))**2
        xf = fftfreq(N, 1 / sr)
        maxpower = np.argmax(yf)
        strongfreq = xf[maxpower]
        dom_f.append(strongfreq)
        time.append(0.1*counter)

        counter += 1
        samples_wrote += buffer
# Finding the minimum, maximum, dominant and average frequencies for the whole audio file.
    x = []
    if min(dom_f) < 20:
        while min(dom_f) < 20:
            dom_f.remove(min(dom_f))
    x.append(dom)
    x.append(max(dom_f))
    x.append(min(dom_f))
    x.append(sum(dom_f)/len(dom_f))
# Reading the csv file to extract the informatin about the 10 different species
    species=[]
    dom_freq=[]
    max_freq=[]
    min_freq=[]
    average_freq=[]
    with open("BirdData.csv") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            species.append(row[0])
            dom_freq.append(int(row[1]))
            max_freq.append(int(row[2]))
            min_freq.append(int(row[3]))
            average_freq.append(int(row[4]))
#Calculating the difference between the audio recording and each species in the database.
    deviations=[]
    for i in range(0,len(dom_freq)):
        deviation = (abs(x[0]-dom_freq[i])+abs(x[1]-max_freq[i])+abs(x[2]-min_freq[i])+abs(x[3]-average_freq[i]))/4
        deviations.append(deviation)
# Finding the smallest difference and outputting the predicted species
    indx = np.argmin(deviations)
    print("The song is the song of a",species[indx])