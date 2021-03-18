import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import librosa.display
from pydub import AudioSegment
import soundfile

def freq_change(audiofile):
    #modified code from: https://stackoverflow.com/questions/60105626/split-audio-on-timestamps-librosa
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
        #create a 0.1 second block of the audio data
        block = audio[int(samples_wrote) : int((samples_wrote + buffer))]
        #perform a FFT to find the dominant frequency per 0.1 second
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
    #x is a list containing the minimum, maximum and average frequency
    return x

def freq_graph(audiofile):
    #modified code from: https://stackoverflow.com/questions/60105626/split-audio-on-timestamps-librosa
    dom_f = []
    time = []
    audio, sr = librosa.load(audiofile)

    #get number of samples for 0.1 seconds
    buffer = 0.1 * sr

    samples_total = len(audio)
    samples_wrote = 0
    counter = 1

    while samples_wrote < samples_total:
        #check if the buffer is not exceeding total samples
        if buffer > (samples_total - samples_wrote):
            buffer = samples_total - samples_wrote
        #create a 0.1 second block of the audio data
        block = audio[int(samples_wrote) : int((samples_wrote + buffer))]
        #perform a FFT to find the dominant frequency per 0.1 second
        N = len(block)
        yf = np.abs(fft(block))**2
        xf = fftfreq(N, 1 / sr)
        maxpower = np.argmax(yf)
        strongfreq = xf[maxpower]
        dom_f.append(strongfreq)
        time.append(0.1*counter)

        counter += 1
        samples_wrote += buffer
    #plot dominant frequency per 0.1 second over time
    plt.figure(figsize=(14, 14))
    plt.plot(time, dom_f)
    plt.ylim((0,int(max(dom_f)+500)))
    plt.xlabel('Time, s')
    plt.ylabel('Dominant frequency, Hz')
    plt.title(audiofile.split('Database Files/')[1])
    plt.show()
