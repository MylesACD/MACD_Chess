

from sklearn import tree
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier as RFC

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd
import PGN_To_Boards as ptb



def single_tree():
   
    
    clf = tree.DecisionTreeClassifier()
    clf.fit(xt,yt)
    
   
    prediction = clf.predict(xv)
    stats = metrics.classification_report(yv,prediction,digits=3)
    print(stats)
    return clf
    
def forest(num_trees):
    clf = RFC(n_estimators = num_trees)
    clf.fit(xt,yt)
    
    print(num_trees," complete")
    return clf
    
    
def plot_roc(clf, x_test, y_test, num_classes, figsize=(17, 6)):
    y_score = clf.predict_proba(x_test)

    # structures
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    classes=["White Win","Tie","Black Win"]
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
    ax.set_title('Receiver operating characteristic of 200 Tree Forest')
    for i in range(num_classes):
        ax.plot(fpr[i], tpr[i], label="ROC curve (area = "+ str(round(roc_auc[i],3)) + ") for class: " + classes[i])
    ax.legend(loc="best")
    ax.grid(alpha=.4)
    plt.show()

#plot the accuracy of several forest sizes
def plot_acc():
    plt.figure()
    sizes = [1,20,50,100,200,400,700]    
    accs=[]
    for size in sizes:
        accs.append(forest(size).score(xv,yv))
    plt.xlabel("Size of Forest")
    plt.ylabel("Accuracy")
    plt.plot(sizes,accs)

    
if __name__ == "__main__":   
    #rebuild the sets with 
    ptb.build_sets(3000, 0.2)
    
    t_set = open("training set.txt","r",encoding="utf-8")
    training = np.array([line.replace("\n","").split(",") for line in t_set])
    xt = training[:,:-1]
    yt = training[:,-1]


    v_set = open("validation set.txt","r",encoding="utf-8")
    validation = np.array([line.replace("\n","").split(",") for line in v_set])
    xv = validation[:,:-1]
    yv= validation[:,-1]

    
    clf = forest(200)
    
    #predictions using the 200 forest
    training_pred = clf.predict(xt)
    validation_pred = clf.predict(xv)
    
    print(metrics.classification_report(yt,training_pred,digits=3))
    print(metrics.classification_report(yv,validation_pred,digits=3))
    
    plot_roc(clf, xv, yv, num_classes=3, figsize=(16, 9))
    plot_acc()
