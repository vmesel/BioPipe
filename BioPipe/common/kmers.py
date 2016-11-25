# File for getting the K-Mers of the FASTA files!
# Made with Python 3.5.1
import pandas as pd
from collections import Counter as cnt
from klib import *


class FileProcessor:

    def GetFileContent(self, file):
        f = open(file, "r")
        return f


    def GetSeparatedRNAs(self, file):
        """
        Pega todos os RNAS e os Separa dos IDs
        """
        content = FileProcessor().GetFileContent(file)
        RNAId = []
        pureRNAs = []
        for line in content:
            if line.startswith(">") is True:
                RNAId.append(line)
            else:
                line = line.replace("\n", "")
                line = line.replace(">", "")
                pureRNAs.append(line)
        return RNAId, pureRNAs


    def GetRNAsLens(self, file):
        """
        Pega o tamanho de cada KMer
        """
        ids, rnas = FileProcessor().GetSeparatedRNAs(file)
        lens = []
        for item in rnas:
            lens.append(len(item))
        return(lens)


    def GetKmerHash(self, file, kn):
        """
        Cria uma hash de KMers
        """
        import textwrap
        RNAIDs, rnas = FileProcessor().GetSeparatedRNAs(file)
        dictslist = []
        for rnaid in range(len(RNAIDs)):
            dk = dict(cnt(textwrap.wrap(rnas[rnaid], kn)))
            dk['LNCRNAID'] = RNAIDs[rnaid].replace("\n","").replace(">", "")
            dk['FILE'] = str(file)
            dictslist.append(dk)
        return dictslist

    def DataFrameLncRNA(self, file, kn):
        #TODO Fazer DataFrame com as contagens dos modulos
        """
        DataFrame feito com os LNCRNAs
        """
        df = pd.DataFrame(FileProcessor().GetKmerHash(file, kn), columns=klib().lista_kmers(kn))
        df.fillna(0, inplace=True)
        return df

    def DataFrameLncRNASampling(self, file, kn, samplenum):
        #TODO Fazer DataFrame com as contagens dos modulos
        """
        DataFrame feito com os LNCRNAs
        """
        df = pd.DataFrame(FileProcessor().GetKmerHash(file, kn), columns=klib().lista_kmers(kn))
        df.fillna(0, inplace=True)
        return df.sample(n=samplenum)

    def DataframeConcatenateSampling(self, file1, file2, kn, samplenum):
        df1 = FileProcessor().DataFrameLncRNASampling(file1, kn, samplenum)
        df2 = FileProcessor().DataFrameLncRNASampling(file2, kn, samplenum)
        df3 = pd.concat([df1, df2])
        return df3

    def DataframeConcatenateMultKMers(self, file1, file2, kn, samplenum):
        dflist = []
        for i in kn:
            df1 = FileProcessor().DataFrameLncRNASampling(file1, i, samplenum)
            df2 = FileProcessor().DataFrameLncRNASampling(file2, i, samplenum)
            df3 = pd.concat([df1, df2])
            dflist.append(df3)
        df4 = pd.concat(dflist)
        df4.fillna(0, inplace=True)
        #print df4
        return df4.to_csv(file1 + "-" + file2 + "-kmers" + str(kn) + "-samples-" + str(samplenum) + ".csv", index=False)

    def DataframeConcatenate(self, file1, file2, kn):
        df1 = FileProcessor().DataFrameLncRNA(file1, kn)
        df2 = FileProcessor().DataFrameLncRNA(file2, kn)
        df3 = pd.concat([df1, df2])
        return df3

    def GetCSVFile(self, file, kn):
        df = FileProcessor().DataFrameLncRNA(file, kn)
        #print 'teste', "LNCRNAID" in df.columns.values
        df.to_csv(file + ".csv", index=False)
        return True
        #return 0

    def GetConcatenatedCSV(self, file1, file2, kn, outputfile):
        df = FileProcessor().DataframeConcatenate(file1, file2, kn)
        #file = str(file1) + str(file2) + "-kmer-" + str(kn)
        df.to_csv(outputfile, index=False)
        return True

#print(FileProcessor().DataFrameLncRNA("teste_ar_associated.fasta", 2))
#print datetime.datetime.now()
#print(FileProcessor().DataframeConcatenateSampling("seq_ar_associated.fasta", "seq_igg_associated.fasta", 8, 100))
#print datetime.datetime.now()
#print(FileProcessor().GetConcatenatedCSV("seq_ar_associated.fasta", "seq_igg_associated.fasta", 5))
#print(FileProcessor().GetConcatenatedCSV("seq_ar_associated.fasta", "seq_igg_associated.fasta", 6))
#print(FileProcessor().GetConcatenatedCSV("seq_ar_associated.fasta", "seq_igg_associated.fasta", 7))
#print(FileProcessor().GetConcatenatedCSV("seq_ar_associated.fasta", "seq_igg_associated.fasta", 5))
#print(FileProcessor().GetConcatenatedCSV("seq_ar_associated.fasta", "seq_igg_associated.fasta", 6))
#print(FileProcessor().GetConcatenatedCSV("seq_ar_associated.fasta", "seq_igg_associated.fasta", 7))
#print(FileProcessor().GetConcatenatedCSV("seq_AR.fasta", "seq_IGG.fasta", 8))
#print(FileProcessor().GetConcatenatedCSV("seq_ar_associated.fasta", "seq_igg_associated.fasta", 9))
#print(FileProcessor().GetConcatenatedCSV("seq_ar_associated.fasta", "seq_igg_associated.fasta", 10))