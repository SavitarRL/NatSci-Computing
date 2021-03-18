import csv
import pandas as pd
import os
import numpy as np
import random

def get_chord_data_matrix():
    with open('chord_info.csv') as f:
        b = csv.reader(f)
        next(b)
        mat = [] ## initializing matrix
        for row in b:
            freq_list = []
            freq_list.append(row[0])
            for idx in range(1,len(row)): #changing from string to float
                if row[idx] == '':
                    freq_list.append(int(0))
                else:
                    freq_list.append(float(row[idx]))
            mat.append(freq_list)
    return mat # returns a  12 x 9 matrix


def bin_search(val, corr):
    #binary search returning the row and column index
    ## mat[row.idx][col.idx]
    ## searching 12 x 8 matrix
    matrix = get_chord_data_matrix()
    assert (len(matrix) != 0), "Error in obtaining matrix"
    mat_str = np.array(matrix)[0: , 1:] ## converted to string somehow
    mat_o = mat_str.astype(np.float)
    mat = np.transpose(mat_o) ## convert to sorted array ##bonary search only works for sorted array


    ## pretend its a 1D array
    row_len = len(mat)         # supposing the row length is the number of groups
    col_len = len(mat[0])      # supposing the col length is the number of elements in a group
    l = 0                   #first index of the 1D array
    h = row_len * col_len   #last index of the 1D array

    lo_target = val - corr ## lower bound
    hi_target = val + corr ## upper bound

    while l<h:
        midpt = (l+h)//2 ## mid point of the 1D array

        row_idx = midpt//col_len ## which group does it belong to
        col_idx = midpt % col_len ## what is its index of that group


        if mat[row_idx][col_idx] >= lo_target and mat[row_idx][col_idx] <= hi_target:
            return col_idx, row_idx ## returns the index if a match is found

        elif mat[row_idx][col_idx] < lo_target:
            l = midpt+1   ## if the scanned element is smaller than the target, we look to the right side of the 1D array
                          ## push up lower bound to the midpt+1

        elif mat[row_idx][col_idx] > hi_target:
            h = midpt     ## if the scanned element is greater than the target, we look to the left

    return 0,0  ## returns both zeros if nothing is identified

def lower_nearest_notes(val, corr): ## returning nearby notes
    row_idx, col_idx = bin_search(val, corr)
    while row_idx == 0 and  col_idx== 0:
        row_idx, col_idx = bin_search(val-corr, corr)
        corr += 1
    return row_idx, col_idx

def higher_nearest_notes(val,corr):
    row_idx, col_idx = bin_search(val, corr)
    while row_idx == 0 and  col_idx== 0:
        row_idx, col_idx = bin_search(val+corr, corr)
        corr += 1
    return row_idx, col_idx

def nearest_notes_idx(val,corr):
    return lower_nearest_notes(val, corr), higher_nearest_notes(val,corr)

def get_chord_note(freq, corr):
    mat = get_chord_data_matrix()
    val = freq
    row_idx, col_idx = bin_search(val, corr)
    if row_idx==0 and col_idx==0:
        return False
    return mat[row_idx][0]

def get_chord_octave(freq, corr):
    mat = get_chord_data_matrix()
    val = freq
    row_idx, col_idx = bin_search(val, corr)
    if row_idx==0 and col_idx==0:
        return False
    return col_idx

def suggest_note_info(freq, corr):
    mat = get_chord_data_matrix()
    lower, higher = nearest_notes_idx(freq,corr)

    lower_idx = lower[0] ; lower_octave = lower[1]
    higher_idx = higher[0] ; higher_octave = lower[1]

    lower_freq = mat[lower_idx][lower_octave+1]
    higher_freq = mat[higher_idx][higher_octave+1]

    lower_note = mat[lower_idx][0]
    higher_note = mat[higher_idx][0]

    print("Unidentified frequency: {} Hz".format(freq))
    print("Choose lower or higher notes")
    print("Possible matches: \nLower frequency({}Hz): Note: {} Octave: {}".format(lower_freq, lower_note, lower_octave))
    print("Higher frequency({}Hz): Note: {} Octave: {}".format(higher_freq, higher_note, higher_octave))

    return None

def nearest_note(freq, corr): ## returns closest frequency
    mat = get_chord_data_matrix()
    lower, higher = nearest_notes_idx(freq,corr)

    lower_idx = lower[0] ; lower_octave = lower[1]
    higher_idx = higher[0] ; higher_octave = lower[1]

    lower_freq = mat[lower_idx][lower_octave+1]
    higher_freq = mat[higher_idx][higher_octave+1]

    lower_note = mat[lower_idx][0]
    higher_note = mat[higher_idx][0]

    hi_freq_diff = higher_freq - freq
    lo_freq_diff = freq - lower_freq

    if hi_freq_diff < lo_freq_diff:
        print("Nearest frequency: {}Hz --> Note: {} Octave: {}".format(higher_freq, higher_note,  higher_octave))
        return higher_freq, str(higher_note), higher_octave

    elif lo_freq_diff < hi_freq_diff:
        print("Nearest frequency: {}Hz --> Note: {} Octave: {}".format(lower_freq, lower_note, lower_octave))
        return lower_freq, str(lower_note), lower_octave
    else:
        suggest_note_info(freq, corr)
        return None

def get_note_info(freq, corr = 3, get_nearest = True):
    ## inputs: frequency: output of the dominant_freq_ext(audiofile); 
    ##         corr: the adjustments/margin/corrections of allowed error, adjustable for accuracy;                          default = 3         **might need to set correction bounds
    ##         get_nearest: returning nearest note; if True: nearest note returned, if False:                                     suggestions returned; default = True

    if freq <= 27.5-corr:
        print("Frequency too low")
        return freq, None, None
    elif freq >= 7902.08 + corr:
        print("Frequency too high")
        return freq, None, None

    else:
        mat = get_chord_data_matrix()
        note = get_chord_note(freq, corr)
        octave = get_chord_octave(freq, corr)

        if note == False or octave == False:
            if get_nearest == 1:
                return nearest_note(freq, corr)
            elif get_nearest ==0:
                return suggest_note_info(freq, corr)
            else:
                raise ValueError('Invalid input: ON --> 1 ; OFF --> 0')
        return str(freq[0])+"Hz", str(note), octave
        ## returning frequency, Note ; Octave


def test_get_note_info(corr, cases = 10 ,runtime = 1):
    start_time = time.time()
    fixed_input = [328.625, 38.891, 2091,7,221.89,987.65,166666,0,475,7700, 979]
    r_in_list = []

    for i in range(cases):
        rand_input = round(random.uniform(5.000, 9000.000), 3)
        r_in_list.append(rand_input)
    print(r_in_list,"\n")

    for freq in r_in_list:
        print(get_note_info(freq, corr, 1))
        print("-"*50)
    for freq in fixed_input:
        print(get_note_info(freq, corr, 1))
        print("-"*50)
    if runtime == 1:
        print("Runtime: --- %s seconds ---" % (time.time() - start_time))
    elif runtime == 0:
        pass
    else:
        raise ValueError("Invalid input {}, must be 1 or 0".format(runtime))
