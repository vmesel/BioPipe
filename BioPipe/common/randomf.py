# File made to support the machlearn section of the lib
# Made with Python 2.7

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score, train_test_split
#from sklearn.metrics import f1_score
import pandas as pd

# Alternative mode!
# from kmers.FileProcessor import *

def ClassificadorRF(KMERFILE, CLASSEDIFERENCIAL):
    #print "IMPORTANDO DADOS"
    dados = pd.DataFrame.from_csv(KMERFILE)
    dados.fillna(value=0)

    #print "MONTANDO OS FEATURES"
    features = [f for f in dados.columns.values if f != "FILE" and f != "LNCRNAID"]
    #print "MONTANDO O RANDOM FOREST"

    dados['FILE'] = dados['FILE'].apply(lambda x: 1 if CLASSEDIFERENCIAL in x else 0)

    train, test = train_test_split(dados, test_size=0.2)

    # Monta o modelo de classificador GINI
    cls = RandomForestClassifier(1000, criterion='gini', warm_start=False, verbose=1, n_jobs=10, oob_score=True, class_weight='auto')
    cls.fit(train[features], train['FILE'])

    # Cross score

    # Monta a cross score(score de validacao de dados)
    cross_score = cross_val_score(cls, test[features][:], test['FILE'][:], cv =5, scoring='f1')

    print cross_score
    print 'cross-validation:', cross_score.mean()

    #
    #sorted_features_importance = sorted([[f, v] for f,  v in zip(features, cls.feature_importances_)], key= lambda x:x[1], reverse=True)
    #contribution_data = pd.DataFrame({'Feature': [x[0] for x in sorted_features_importance],'Value': [float(x[1]) for x in sorted_features_importance]})
    #print contribution_data