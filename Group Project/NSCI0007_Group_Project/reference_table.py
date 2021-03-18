import pandas as pd
import os
import frequency_time
import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import librosa.display
from pydub import AudioSegment
import soundfile


def freq_change(audiofile):
    #source code: https://stackoverflow.com/questions/60105626/split-audio-on-timestamps-librosa
    dom_f = []
    time = []
    audio, sr = librosa.load(audiofile)

    # Get number of samples for 0.1 seconds
    buffer = 0.1 * sr

    samples_total = len(audio)
    samples_wrote = 0
    counter = 1

    while samples_wrote < samples_total:
        #check if the buffer is not exceeding total samples
        if buffer > (samples_total - samples_wrote):
            buffer = samples_total - samples_wrote

        block = audio[int(samples_wrote) : int((samples_wrote + buffer))]

        N = len(block)
        yf = np.abs(fft(block))**2
        xf = fftfreq(N, 1 / sr)
        maxpower = np.argmax(yf)
        strongfreq = xf[maxpower]
        dom_f.append(strongfreq)
        time.append(0.1*counter)
        
        counter += 1
        samples_wrote += buffer
        
    x = []
    #filtering out frequencies below 20 Hz as this is below the human range of hearing
    if min(dom_f) < 20:
        while min(dom_f) < 20:
            dom_f.remove(min(dom_f))
    x.append(min(dom_f))
    x.append(max(dom_f))
    x.append(sum(dom_f)/len(dom_f))
    return x


# code for how we created the bird database

reference_table = pd.DataFrame( columns = ['species',  'minimum_frequency', 'maximum_frequency', 'average_frequency']) #create an empty table

os.chdir('/home/user/Assessments/NSCI0007_Group_Project/Database Files') #set the current working directory to the one containing the audiofile
audiofiles = os.listdir() #list of all the audiofiles in the working dir
maxf, minf, fbar, species= [], [], [], [] #create 4 empty lists corresponding to the columns in the table
for audiofile in audiofiles:
    print(audiofile)
    #fill in the lists using string manipulation and the output of the frequency function
    species.append(audiofile.split('.')[0])
    minf.append(freq_change(audiofile)[0])
    maxf.append(freq_change(audiofile)[1])
    fbar.append(freq_change(audiofile)[2])

reference_table['species'] = species
reference_table['maximum_frequency'] = maxf
reference_table['minimum_frequency'] = minf
reference_table['average_frequency'] = fbar

reference_table

reference_table.to_pickle('Reference Table')

pd.read_pickle('Reference Table')



