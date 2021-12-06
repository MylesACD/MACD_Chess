import PGN_To_Boards as ptb

from sklearn import tree
import State as s
import Move as m
import numpy as np



def single_tree():
    t_set = open("training set.txt","r",encoding="utf-8")
    training = np.asarray([line.rstrip().split(",") for line in t_set])
    
    xt = training[:,:-1]
    yt = training[:,-1]
    clf = tree.DecisionTreeClassifier()
    
    clf.fit(xt,yt)
    
    v_set = open("validation set.txt","r",encoding="utf-8")
    validation = np.array([line.rstrip().split(",") for line in v_set])
    xv = validation[:,:-1]
    yv= validation[:,-1]
    
    
    prediction = clf.predict(xv)
    print(prediction==yv)
    
single_tree()