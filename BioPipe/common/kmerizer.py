from kpal.klib import Profile
from tqdm import tqdm
import pandas as pd


def sequence_to_kmer(genome_str, k, hash_kmer=False):
    p = Profile.from_sequences([genome_str], k)
    if not hash_kmer:
        return p
    else:
        hash_out = {}
        for i in range(4 ** k):
            hash_out[p.binary_to_dna(i)] = p.counts[i]
        return hash_out


def read_fasta_and_iterate(fasta, classname, kmer):
    kmerize = open(fasta, "r")
    kmer_full_hash = {}
    dnalist = []
    seqlist = []
    for line in kmerize.readlines():
        if line.startswith(">"):
            dnalist.append(line.replace(">", "").replace("\n",""))
        else:
            seqlist.append(line)
    for dna, seq in tqdm(zip(dnalist, seqlist)):
        kmer_full_hash[dna] = sequence_to_kmer(seq, kmer, hash_kmer=True)
    kmer_full_hash["FILE"] = classname
    return kmer_full_hash


def mount_pandas_df(fasta, classname, kmer):
    hash = read_fasta_and_iterate(fasta, classname, kmer)
    ids = []
    values_hash = []


    for key, value in hash.iteritems():
        ids.append(key)
        values_hash.append(value)

    for value, id in zip(values_hash, ids):
        try:
            value["LNCRNAID"] = str(id)
            value["FILE"] = str(classname)
        except:
            i = values_hash.index(value)
            values_hash.pop(i)

    df = pd.DataFrame(values_hash)
    df = df.set_index(["LNCRNAID"])
    return df

def get_two_fastas_csv(fasta, classname, fasta2, classname2, kmer, outputfile):
    print classname
    df1 = mount_pandas_df(fasta, classname, kmer)
    print classname2
    df2 = mount_pandas_df(fasta2, classname2, kmer)
    df3 = pd.concat([df1, df2])
    return df3.to_csv(outputfile)


# print sequence_to_kmer("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", 6, hash_kmer=True)
# #print get_two_fastas_csv("/home/vinicius/BigWig/useful/material/outputs/seq_ARA.fasta", "ARA",
#                       "/home/vinicius/BigWig/useful/material/outputs/seq_IGA.fasta", "IGA", 6, "output-kmerizacao-6.csv")