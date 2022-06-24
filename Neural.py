
from sklearn import tree
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import StandardScaler


import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns
import PGN_To_Boards as ptb
import State as s
import pickle

scaler = StandardScaler()

t_set = open("training set.txt","r",encoding="utf-8")
training = np.array([line.replace("\n","").split(",") for line in t_set],dtype=int)
xt = training[:,:-1]
yt = training[:,-1]
scaler.fit(xt)
xt = scaler.transform(xt)


v_set = open("validation set.txt","r",encoding="utf-8")
validation = np.array([line.replace("\n","").split(",") for line in v_set],dtype=int)
xv = validation[:,:-1]
yv= validation[:,-1]
xv = scaler.transform(xv)


def plot_roc(clf, x_test, y_test, num_classes, figsize=(17, 6)):
    y_score = clf.predict_proba(x_test)

    # structures
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    # calculate dummies once
    y_test_dummies = pd.get_dummies(y_test, drop_first=False).values
    for i in range(num_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_dummies[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # roc for each class
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('Receiver operating characteristic example')
    for i in range(num_classes):
        ax.plot(fpr[i], tpr[i], label='ROC curve (area = %0.2f) for label %i' % (roc_auc[i], i))
    ax.legend(loc="best")
    ax.grid(alpha=.4)
    sns.despine()
    plt.show()

def think():
    clf = MLPClassifier().fit(xt,yt)
    print("net completed")
    filename = "MLPC.sav"
    pickle.dump(clf, open(filename,"wb"))
    
    return clf

if __name__ == "__main__":   
    #clf = think()
    """
    test1 = "1. e3 d5 2. c3 f5 3. Bb5+ Qd7"
    test2 = "1. e3 d5 2. c3 f5 3. Bb5+ Qd7 4. Bxd7+"
    test3 = "1. e3 d5 2. c3 f5 3. Bb5+ Qd7 4. Bxd7+ Kf7 5. Bxc8 Kg6 6. Qb3 Kg5 7. Qxb7 Kf6 8. Qxa8"
    state1 = ptb.single_state(test1)
    state2 = ptb.single_state(test2)
    state3 = ptb.single_state(test3)
    print(clf.predict_proba(state1))
    print(clf.predict_proba(state2))
    print(clf.predict_proba(state3))
    """
    clf = pickle.load(open("MLPC.sav", 'rb'))
    
    pred1 = clf.predict(xt)
    pred2 = clf.predict(xv)
    print(metrics.classification_report(yt,pred1,digits=3))
    print(metrics.classification_report(yv,pred2,digits=3))
    
    plot_roc(clf, xv, yv, num_classes=3)
    