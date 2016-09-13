import pandas as pd
from scipy.stats import zscore

from fastagen import fastageneratorlist


def RunZScoreAlgorithm(filename, separator):
    a = pd.read_csv(filename, sep=separator)
    a["zscore_mean"] = zscore(a["MEDIA"].values)
    print("CALCULA ZSCORE")
    return a

def RemoveTargetZScores(filename, separator, target):
    a = RunZScoreAlgorithm(filename, separator)
    qq = "zscore_mean " + str(target)
    print("FILTRA ZSCORE")
    return a.query(qq)

def GenerateZScoreFile(filename, separator, output):
    a = RunZScoreAlgorithm(filename, separator)
    #print("AQUI")
    a.to_csv(output)

def GenerateFasta(filename, separator, target, outputfasta):
    print("GERA O FASTA")
    #try:
    outputZscore = [x for x in RemoveTargetZScores(filename, separator, target)["Features"]]
    if outputZscore == []:
        print("Por favor altere a zscore para poder pegar valores")
    else:
        fastageneratorlist(outputZscore, outputfasta)


