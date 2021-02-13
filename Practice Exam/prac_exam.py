import numpy as np
import matplotlib.pyplot as plt
import math as m
import os

def overlap(x,y): #return overlap between strings x & y
    for n in range(len(x)):
#         print(x[-n:], y[:n])
        if x[-n:] == y[:n]:
#             print(x[-n:], y[:n])
            break
        else:
            n=0
    return n

def test_overlap():
    n1 = overlap("XXXABC", "ABCYYY")
    n2 = overlap("ABCYYY", "XXXABC")
    n3 = overlap("XXXABC", "ABC")
    assert(n1 ==3 and n2 == 0 and n3 == 3),"overlap incorrect"
    print(n1,n2,n3, "pass overlap")

def merge(x,y):
    #returns a string formed by overlapping the two strings x&y
    idx_rm = overlap(x,y)
    print("Remove from:", idx_rm)
    string = x+y[idx_rm:len(y)]
    return string

def test_merge():
    s1 = merge("XXXABC", "ABCYYY")
    s2 = merge("ABCYYY", "XXXABC")
    s3 = merge("XXXABC", "ABC")
    assert(s1 == "XXXABCYYY" and s2=="ABCYYYXXXABC" and s3 == "XXXABC"), "merge fail"
    print(s1, s2, s3, "pass merge")

def longest_overlap(string_list): #returns[pair1.idx, pair2.idx, overlap]
    # print("The list: ", string_list,"\n")
    length = len(string_list)
    # print("length: ", length)
    comp_dict = {} #(pair, overlap)
    trynum = 0
    for item in string_list:
        for k in range(length):
            # print("k: ", k)
            first = string_list.index(item)
            nextone = k
            if nextone != first and nextone < length: #overiding the list index out of range error
                idx_overlap = overlap(item, string_list[nextone])
                trynum += 1
                # adi +=1
                # print("Pair 1: {}; Pair 2: {}; overlap num: {}".format(first , nextone, idx_overlap))
                comp_dict[str(first) + str(nextone) + str(trynum)] = idx_overlap 
                # print("first: {}; second: {}; Trial number: {}; overlap_index: {} \n".format(first, nextone, trynum ,idx_overlap))
    print("Pair: overlap {} \n".format(comp_dict)) 
    comp_val = list(comp_dict.values())
    k = (max(comp_val))
    k_idx = comp_val.index(k)
    # print("maximum overlap value: ", k)
    # print("max overlap: ", k_idx)
    comp_keys = list(comp_dict.keys())
    # print("dict_keys: ", comp_keys)
    trio = comp_keys[k_idx]
    # print("Keys of the max: ", trio)
    i = int(trio[0]); j= int(trio[1])
#     print(i,j,k)
    return [i,j,k]

def test_longest_overlap():
    i, j, k = longest_overlap(["XXXABC", "ABCYYY", "BC"])
    assert(i==0 and j==1 and k==3), "longest_overlap fail"
    print(i , j, k, "pass longest_overlap")
    

def identify_strand(fragment_list, n): #returns list
    # repeatedly applies the longest_overlap function to the list fragment_list
    frag_list= fragment_list 
    
    length = len(frag_list)
    pair1, pair2, overlap_idx = longest_overlap(frag_list)
    print("pair1 idx: {}; pair2 idx {}; overlap num: {}".format(pair1, pair2,overlap_idx))
    print("length:", length)
    if overlap_idx > n:
        print("Original frag list: {}".format(frag_list))
        pair_1st = frag_list[pair1] 
        pair_2nd = frag_list[pair2]
        print("Pair1: {}; Pair2: {}".format(pair_1st, pair_2nd))
        new_str = merge(pair_1st , pair_2nd)
        print("new string: ",new_str)
        # for elem in frag_list:
        #     if elem == frag_list[pair1] or elem == frag_list[pair2]
        # frag_list.remove(frag_list[pair1]); frag_list.remove(frag_list[pair2])
        # frag_list.pop(pair1); frag_list.pop(pair2)
        frag_list.remove(pair_1st) 
        frag_list.remove(pair_2nd)
        frag_list.append(new_str)
        print("new frag list: {} \n".format(frag_list))
        if len(frag_list) >1:
            identify_strand(frag_list, n)
        elif length == 1:
            print("final? frag_list: {}\n".format(frag_list))
            return frag_list
    sorted(frag_list, key = len)
    return frag_list[-1]
    
    # if the longest overlap is n or greater, then the code should:
    # 1. remove the two identified strings from the list.
    # 2. merge the two strings and append the merged string to the list.

    # function terminates when list contains only a single string OR the longest overlap is strictly less than n
    

def test_identify_strand():
    simple_dna = ['tgaaaattcctttctattttaggccc', 
                'tgaaaattcctttctattttaggcccatgcaat', 
                'ggcattagggcggttaa', 'atgcaatggcattagggcggttaa',   
                'ggttaa', 'tgaaaattcctttctattt', 
                'taggcccatgcaatggcattagggc']
    s = identify_strand(simple_dna, 4)
    print("Answer string: {}\n".format(s))
    assert(s=='tgaaaattcctttctattttaggcccatgcaatggcattagggcggttaa'), "identify_strand fail"
    print("pass identify_strand")

def test_modify():
    pass

def test():
    print("Test results:")
#     test_overlap() #q1
#     test_merge() #q2
    # test_longest_overlap() #q3
    # i,j,k = longest_overlap(['tgaaaattcctttctattttaggccc', 
    #                         'tgaaaattcctttctattttaggcccatgcaat', 
    #                         'ggcattagggcggttaa', 'atgcaatggcattagggcggttaa', 
    #                         'ggttaa', 'tgaaaattcctttctattt', 
    #                         'taggcccatgcaatggcattagggc'])
    # print(i,j,k)
    test_identify_strand() #q4
def main():
    pass


if __name__ == "__main__":
    test()
    
    