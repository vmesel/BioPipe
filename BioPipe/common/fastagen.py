import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt


#sns.set_style("whitegrid")

def fastagenerator(filename, outputfasta):
    df = pd.read_csv(filename,sep='\t')
    f = open(outputfasta, "w")
    x = [feature for feature in df["Features"]]
    z = [zscore for zscore in df["MEDIA"]]
    for zscore in z:
        for feature in x:
            f.write(">kmer_" + str(feature) + "\n")
            f.write(feature + "\n")
    f.close()

def fastageneratorlist(x, outputfasta):
    f = open(outputfasta, "w")
    for feature in x:
        f.write(">kmer_" + str(feature) + "\n")
        f.write(feature + "\n")
    f.close()
    return True

def top10generator(filename):
    df = pd.read_csv(filename, sep=',')
    df1 = df.nlargest(10, 'zscore_mean')[['Features', 'zscore_mean']]
    df2 = df.nsmallest(10, 'zscore_mean')[['Features', 'zscore_mean']]
    df2 = df2.sort_values(by="zscore_mean", ascending=False)
    df3 = pd.concat([df1, df2])
    df3.set_index("Features")
    return df3
    #color_list = df3['zscore_mean'].apply(lambda c : 'red' if c >0 else 'blue')
    #flatui = color_list
    #sns.barplot(x='zscore_mean', y='Features', data=df3, palette=sns.color_palette(flatui))
    #plt.title("Kmer x ZScore Value")
    #namefig = "/var/www/vinicius/DadosPaper/comparacao-kmers.png"
    #plt.show()
    #plt.savefig(namefig)
    #print df3

#print("Gerando Fasta de KMer Tamanho 6")
#fastagenerator("/work/users/vinicius/GitHub/BioInfo/DadosPaper/csvsvalidados/kmer_6_repeticoes_10.csv", "/work/users/vinicius/GitHub/BioInfo/FastaGenerator/kmer_6_repeticoes_10.fasta")
#print("Gerando Fasta de KMer Tamanho 7")
#fastagenerator("/work/users/vinicius/GitHub/BioInfo/DadosPaper/csvsvalidados/kmer_7_repeticoes_10.csv", "/work/users/vinicius/GitHub/BioInfo/FastaGenerator/kmer_7_repeticoes_10.fasta")
#print("Gerando Fasta de KMer Tamanho 8")
#fastagenerator("/work/users/vinicius/GitHub/BioInfo/DadosPaper/csvsvalidados/kmer_8_repeticoes_10.csv", "/work/users/vinicius/GitHub/BioInfo/FastaGenerator/kmer_8_repeticoes_10.fasta")
#print("Gerando Fasta de KMer Tamanho 9")
#fastagenerator("/work/users/vinicius/GitHub/BioInfo/DadosPaper/csvsvalidados/kmer_9_repeticoes_10.csv", "/work/users/vinicius/GitHub/BioInfo/FastaGenerator/kmer_9_repeticoes_10.fasta")