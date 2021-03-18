import scipy
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq
import sklearn
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

cwd = os.getcwd()

def remove_all_files(folder):
    cwd = os.getcwd()
    dir_path = os.path.join(cwd,folder)
    for files in os.listdir(dir_path):
        os.remove(os.path.join(dir_path,files))
    while True: 
        YesorNo = input("Are you sure you want to delete {}? Y/N".format(dir_path))
        if YesorNo == 'Y':
#             print(file_path)
            os.rmdir(folder) ## reconfirmation so we dont delete the wrong files
            break
        elif YesorNo == 'N': 
            break
        else:
            raise ValueError("Check Y/N")
        break

def check_dir(folder):
    path = os.path.join(cwd, folder)
    if os.path.exists(path) is False:
        os.mkdir(path)
    else:
        pass

def scan_audio_length(song_file):
    audio = AudioSegment.from_wav(song_file)
    return len(audio)/1000 ## audio length in seconds

def pad_audio(song_file, time, length):
    aud = AudioSegment.from_wav(song_file)
    len_silence = (length - time)*1000
    silence = AudioSegment.silent(duration = len_silence)
    padded = aud + silence
    return padded

def cut_audio(song_file, length):
    aud = AudioSegment.from_wav(song_file)
    return aud[0:length*1000]

def clean_audio_files(song_file, length): # making them same lengths
    path = os.path.join("Database Files")
    filename = os.path.join(path , song_file)
    sound_file = AudioSegment.from_wav(filename)
#     print(sound_file)
    time = scan_audio_length(filename)
    cwd = os.getcwd()
    
    if time > length:
        cleaned = cut_audio(filename, length)
    elif time < length:
        cleaned = pad_audio(filename, time, length)
    else:
        pass
    check_dir("cleaned")
    exp_path = os.path.join(cwd, "cleaned")
    cleaned.export(exp_path +"/"+ song_file, format="wav")

def split_equal_audio(song_file, length, parts):
    path = os.path.join(cwd, "cleaned")
    aud_file = os.path.join(path, song_file)
    newAudio = AudioSegment.from_wav(aud_file)
    assert(scan_audio_length(aud_file) == length), "Audio is not {} seconds, current length is {}s".format(length, scan_audio_length(aud_file))
    i = 0
    div = length//parts
    if length%parts != 0:
        raise ValueError("Not split fully")
    while i < length*1000:
        splitAudio = newAudio[i:(i+div)]
        exp_file = os.path.join(cwd, "splits" ,"{}_split{}.wav".format(song_file, int(i/(div*1000))))
        splitAudio.export(exp_file, format="wav")
        i += div*1000

def load_fft_data(song):
    x, sr = librosa.load(song)
    N = len(x)
    yf = np.abs(fft(x))**2
    yfn = fft(x).real
    xf = fftfreq(N, 1 / sr)
#     maxpower = np.argmax(yf)
#     strongfreq = xf[maxpower]
    return yfn, xf ## 0: real fft; 1: frequency

def add_to_PCA():
    cwd = os.getcwd()
    file_path = "splits"
    direct_path = os.path.join(cwd, file_path)
#     print(direct_path)
    ### attributes: 1: fft_real; 2: freq
    power_list = []
    fft_real = []
    freq = []
    birds = []
    birdnames = []
    fft_freq = {}
    dataframe = {}
    count = 0
    fftlength = []

    
    for song in os.listdir(direct_path):
        song_dir = os.path.join(direct_path, song)
        data = load_fft_data(song_dir)
        fftreals = data[0]
#         print(type(len(fftreals)))
        fftlength.append(len(fftreals))
#     print(fftlength)
        
    for song in os.listdir(direct_path):

        song_dir = os.path.join(direct_path, song)
        data = load_fft_data(song_dir)
        birdname = song.split("/")[-1].split(".wav")[0]
        
        fftreals = data[0] ## np array
        freq = data[1]
        for i in data[0]:
#             power_list.append(i)
            birds.append(birdname)
#         print(freq.shape)
#         print(fftreals.shape)

        dataframe[song] = fftreals[0:min(fftlength)] #to have the same array length
#         count += 1
    for elem in birds:
        if elem not in birdnames:
            birdnames.append(elem)
        else:
            continue
    return dataframe, birdnames, min(fftlength)

def get_PCA(mode):

    datadict, birdnames, len_target = add_to_PCA()
    birdies = []

    features = []
    for i in range(len_target):
        features.append('freq num{}'.format(i+1))
#     print(features)

    ffts = datadict.values()
    clips = datadict.keys()
    for elem in clips:
        birdies.append(elem.split(".wav")[0])

    df = pd.DataFrame(data = ffts, columns = features)
    df['Clips'] = birdies
#     print(df)
    x = df.loc[:, features].values
    x = StandardScaler().fit_transform(x)
#     print(x.shape)
    pca = PCA(n_components = 2)
    tsne = TSNE(n_components = 2)
    if mode == "PCA":
        princ_comp = pca.fit_transform(x)
    elif mode == "TSNE":
        princ_comp = tsne.fit_transform(x)
    else:
        raise ValueError("{} is not a valid input. Choose only 'PCA' or 'TSNE'".format(mode))

    princ_df = pd.DataFrame(data = princ_comp,
                            columns = ['PC1', 'PC2'])

    final_data = pd.concat([princ_df, df[['Clips']]], axis = 1)
#     print(final_data)
    return final_data

def plot_PCA(mode):
    data, birdnames, len_target = add_to_PCA()
    fin_data = get_PCA(mode)
#     print(birdnames)
    fig = plt.figure(figsize = (9,9))
    ax = fig.add_subplot(1,1,1)
    if mode == "PCA":
        ax.set_xlabel('Principal Component 1', fontsize = 20)
        ax.set_ylabel('Principal Component 2', fontsize = 20)
    elif mode == "TSNE":
        ax.set_xlabel('TSNE 1', fontsize = 20)
        ax.set_ylabel('TSNE 2', fontsize = 20)
    ax.set_title('2 component {}'.format(mode), fontsize = 25)

    colorlist = ['r', 'g', 'b', 'k', 'm','c', 'y', 'indigo', 'pink', 'peru']
    colors = colorlist[:len(birdnames)]

    for target, color in zip(birdnames,colors):
        bird = fin_data['Clips']
        bird_ident = bird == target #boolean expression

        ax.scatter(fin_data.loc[bird_ident, 'PC1']
                  ,fin_data.loc[bird_ident, 'PC2']
                  ,s=20)
    ax.legend(birdnames)
    ax.grid()

    if mode =="PCA":
        plt.xlim(-7.5,5)
        plt.ylim(-3, 2.7)
    elif mode == "TSNE":
        plt.xlim(-100, 100)
        plt.ylim(-100, 100)

def analyse_PCA_birds(num = 10, rmv = True, length = 30, parts = 6, mode = "PCA"):
    ## num --> range (1-5)
    ## rmv --> remove_all_files(): Yes = True, No = False
    ## length --> length of audio, deafult = 30s
    ## parts --> number of parts wanted to be split, default = 6
    ## mode --> PCA or TSNE analysis, default = 'PCA'

    cwd = os.getcwd()
    path = os.path.join(cwd, "Database Files")
    check_dir("splits")
    filenames = []
    for file in os.listdir(os.path.join(cwd, "Database Files")):
        if file.endswith("wav"):
             filenames.append(file.split(".wav")[0])

    if num > len(filenames)+1:
        raise ValueError("Number of birds {} exceeds existing number of bird songs {}".format(num, len(filenames)))
    elif num == 0:
        raise ValueError("Nothing to compare to.")

    for i in range(num):
#         print(filenames[i]+".wav")
        clean_audio_files(filenames[i]+".wav", length )
        split_equal_audio(filenames[i]+".wav", length, parts)

    plot_PCA(mode)

    if rmv == True:
        remove_all_files("splits")
        remove_all_files("cleaned")

def main():
    analyse_PCA_birds(10, rmv = True, length = 30, parts = 6, mode = 'PCA')
    analyse_PCA_birds(10, rmv = True, length = 30, parts = 6, mode = 'TSNE')


