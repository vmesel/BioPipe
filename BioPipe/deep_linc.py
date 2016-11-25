import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.cross_validation import train_test_split, cross_val_score

def ClassificadorDeep(filename, validationnum, classeDiferencial):
    df = pd.read_csv(filename)

    df['FILE'] = df['FILE'].apply(lambda x: 1 if classeDiferencial in x else 0)

    df = df.drop('LNCRNAID', 1)
    train, test = train_test_split(df, test_size = 0.2)

    features = [f for f in train.columns.values if f != "FILE"]

    clf = MLPClassifier(solver="lbgfs", alpha=1e-5, hidden_layer_sizes=(5, 2), learning_rate="adaptive")
    clf.fit(train[features],  train["FILE"])

    #clf.predict(test[features])

