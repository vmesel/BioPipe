from sklearn import svm
from sklearn.cross_validation import train_test_split, cross_val_score
import pandas as pd
import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt


#sns.set_style("whitegrid")


def ClassificadorSVM(filename, validationnum, classeDiferencial):
    df = pd.read_csv(filename)

    df['FILE'] = df['FILE'].apply(lambda x: 1 if classeDiferencial in x else 0)

    df = df.drop('LNCRNAID', 1)
    train, test = train_test_split(df, test_size = 0.2)

    features = [f for f in train.columns.values if f != "FILE"]

    #Cria o classificador
    classificador = svm.SVC(kernel="linear")

    classificador.fit(train[features],  train["FILE"])

    pddf = pd.DataFrame({'FEATURES': features, validationnum:classificador.coef_[0] })

    #score = classificador.score(test[features], test["FILE"])
    #scorezin = cross_val_score(classificador, df[features][:], df['FILE'][:], cv=5, scoring='f1')
    #print "SVM - Score:" + str(score)
    #print "SVM - F1 Score:" + str(scorezin)

    return pddf


def RodaValidacoes(inputfile, repeticoes, kmer, classeDiferencial, outputfile):
    kmerdf = pd.DataFrame()
    dfwithfile = pd.read_csv(inputfile)
    dfwithfile = dfwithfile.drop('LNCRNAID', 1)
    dfwithfile = dfwithfile.drop('FILE', 1)
    features = dfwithfile.columns.values

    kmerdf['Features'] = features
    reps = int(repeticoes) - 1
    for i in range(reps):
        kmerdf[i] = ClassificadorSVM(inputfile, i, classeDiferencial)[i]

    print("Calculando a media")
    kmerdf["MEDIA"] = kmerdf.mean(axis=1)
    print kmerdf
    kmerdf.to_csv(outputfile, index=False, sep='\t')



