

from sklearn import tree
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier as RFC
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd
import seaborn as sns
import PGN_To_Boards as ptb

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
    print(num_trees," complete")
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


def plot_acc():
    sizes = [1,20,50,100,200,400,700,1000]    
    #accs=[0.38, 0.434, 0.442, 0.449,0.449,0.4495,0.4485,0.451]
    accs=[]
    for size in sizes:
        accs.append(forest(size).score(xv,yv))
    plt.xlabel("Size of Forest")
    plt.ylabel("Accuracy")
    plt.plot(sizes,accs)
    
clf = forest(200)
line ="1. e4 c5 2. c3 Nc6 3. Qg4 Ne5 4. a3"
test = [string.rstrip().split(",") for string in ptb.build_game(line)]
print(clf.predict_proba(test))
#plot_roc(forest(200), xv, yv, num_classes=3, figsize=(16, 9))
#pred = forest(100).predict(xv)
#print(metrics.confusion_matrix(yv,pred))

#print(metrics.classification_report(yv,pred,digits=3))