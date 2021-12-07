

from sklearn import tree
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier as RFC
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd
import seaborn as sns


t_set = open("training set.txt","r",encoding="utf-8")
training = np.asarray([line.rstrip().split(",") for line in t_set])
xt = training[:,:-1]
yt = training[:,-1]

v_set = open("validation set.txt","r",encoding="utf-8")
validation = np.array([line.rstrip().split(",") for line in v_set])
xv = validation[:,:-1]
yv= validation[:,-1]

def single_tree():
   
    
    clf = tree.DecisionTreeClassifier()
    
    clf.fit(xt,yt)
    
   
    
    prediction = clf.predict(xv)
    stats = metrics.classification_report(yv,prediction,digits=3)
    #depth = clf.get_depth()
    
    
    #print("--------------------\n","single tree\n")
    # print(stats)
       # print(depth)
       # print(prediction==yv)
    accuracy = clf.score(xv,yv)
    print(stats)
    return clf
    
def forest(num_trees):
    clf = RFC(n_estimators = num_trees)
    clf.fit(xt,yt)
    
    #prediction = clf.predict(xv)
    #stats = metrics.classification_report(yv,prediction,digits=3)
   # accurracy = clf.score(xv,yv)
   # print("--------------------\n",num_trees," forest\n")
   # print(stats)
    return clf
    
    
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

plot_roc(forest(1000), xv, yv, num_classes=3, figsize=(16, 10))

#single_tree()
