class Genetics:
    def __init__(self, codon, aacid, dna, rna):
        self.stop_codon = stop_codon = ["UAA","UAG","UGA"]
        self.genetic_code = ['GCA', 'GCC', 'GCG', 'GCU', 'UGC', 'UGU', 'GAC', 'GAU', 'GAA',
                'GAG', 'UUC', 'UUU', 'GGA', 'GGC', 'GGG', 'GGU', 'CAC', 'CAU',
                'AUA', 'AUC', 'AUU', 'AAA', 'AAG', 'UUA', 'UUG', 'CUA', 'CUC',
                'CUG', 'CUU', 'AUG', 'AAC', 'AAU', 'CCA', 'CCC', 'CCG', 'CCU',
                'CAA', 'CAG', 'AGA', 'AGG', 'CGA', 'CGC', 'CGU', 'CGG', 'AGC',
                'AGU', 'UCA', 'UCC', 'UCG', 'UCU', 'ACA', 'ACC', 'ACG', 'ACU',
                'GUA', 'GUC', 'GUG', 'GUU', 'UGG', 'UAC', 'UAU', 'UAG', 'UAA','UGA']
        self.amino_acid = ['A', 'A', 'A', 'A', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F',
               'G', 'G', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 'K', 'K', 'L',
               'L', 'L', 'L', 'L', 'L', 'M', 'N', 'N', 'P', 'P', 'P', 'P',
               'Q', 'Q', 'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S', 'S', 'S',
               'S', 'S', 'T', 'T', 'T', 'T', 'V', 'V', 'V', 'V', 'W', 'Y',
               'Y', '!', '!', '!']
        super().__init__()
        self.codon = codon
        self.aacid = aacid
        self.dna = dna
        self.rna = rna
       


    def DNA_seq(self, file):
        dna = []
        with open(file) as f:
            next(f) #skipping first line
            for c in f:
                return c

    def start_pos(self, sequence):
        for i in range(len(sequence)):
            if seq[i:i+3] == "AUG":
                return i

    def print_codon(self,sequence):
        codon = []
        j = int(self.start_pos(sequence))
        for k in range(j+3,len(sequence),3):
            elem = sequence[k:k+3]
            if elem not in self.stop_codon:
                self.codon.append(elem)
            else:
                break
        return codon

    def test_length(self):
        assert(len(self.genetic_code) == len(self.amino_acid)), "Lengths do not match"
        return True

    def __str__(self):
        return self.genetic_code + "\n" + self.stop_codon + "\n" + self.amino_acid

class Translate:
    def __init__(self):
        self.gene = Genetics()
        self.gene = g
        self.seq = seq
        dna_seq = self.gene.DNA_seq(file)
        seq = dna_seq.replace("T","U")

    

    # def dna_to_rna(self, file):
    #     dna_seq = self.gene.DNA_seq(file)
    #     rna = dna_seq.replace("T","U")
    #     return rna

    def trans(self, seq): #translates RNA codon to a list of amino acids
        if test_length(self.genetic_code, self.amino_acid) is True:
            ac_list = []
            codon_list = print_codon(seq)
            for c in codon_list:
                if c in self.genetic_code:
                    codonidx = self.genetic_code.index(c) #getting index of the codon
                    ac_list.append(self.amino_acid[codonidx])
        return ac_list

    def __str__(self):
        return self.seq

class Acid:
    def __init__(self):
        self.acid_list = []
        for item in Genetics.amino_acid:
            if item not in self.acid_list:
                self.acid_list.append(item)
        self.translate = Translate()
        self.translate.seq = seq
    
    def count_amino(self, seq): #returns the frequencies of each amino acid
        count_dict = {}
        count_list = []
        translated_code = Translate.trans(Translate.seq)
        for item in translated_code:
            if item in count_dict:
                count_dict[item] += 1
            else:
                count_dict[item] = 1
        sorted_count = sorted(count_dict)
        for dude in a_list:
            if dude not in count_dict:
                count_list.append(0)
            else:
                count_list.append(count_dict[dude])
        return count_list

    def check_length(self, Translate.seq):
        am_list = self.count_amino(seq, Genetics.genetic_code, Genetics.amino_acid)
        assert(len(self.acid_list) == len(am_list)), "Lengths do not match"
        return True


import matplotlib.pypot as plt
import math as m
import numpy as numpy

def plot(seq):
    y_list = Acid.count_amino(seq)
    x_list = Acid.acid_list
    plt.bar(x_list, y_list)
    plt.ylabel("Frequency")
    plt.xlabel("Amino acids")
    plt.title("Plot of frequency of amino acids")


    



if __name__ == '__main__':
    file = "Simple_gene_new.fasta"
    translate = Translate()
    acid = Acid()
    genetics = Genetics()
    print(translate)
    print(acid.acid_list)
    print(check_length(translate.seq))
    print(count_amino())
    plot(translate.seq)
    plt.show()
    pass


