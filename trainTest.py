#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDClassifier



def trainTest():

    submitFile = open("Submission.csv", "a+")
    dataTest = pd.read_csv("cleanTextFile_test.csv",index_col=0,encoding='utf-8-sig')   #test data


    dataTrain = pd.read_csv('cleanTextFile_train.csv',encoding='utf-8-sig')           #train data
    

    Y=dataTrain[" Sentiment"]
    X = dataTrain.Text.fillna(' ')  #Replace empty string with space 
    Y=Y.astype('int')


    # -----------------------------------Train----------------------------------------

    print "\nTraining the data ...............\n\n"

    text_clf_svm = Pipeline([('vect', CountVectorizer()),                    # Apply SVM classifier algorithm using GridSearchCV for training the text
                      ('tfidf', TfidfTransformer()),
                      ('clf-svm', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, n_iter=10, random_state=42)),])


    parameters_svm = {'vect__ngram_range': [(1, 1), (1, 2)],
               'tfidf__use_idf': (True, False),
               'clf-svm__alpha': (1e-2, 1e-3),
    }

    gs_clf_svm = GridSearchCV(text_clf_svm, parameters_svm, n_jobs=-1)
    gs_clf_svm = gs_clf_svm.fit(X,Y)



    #--------------------------------------Test------------------------------------------

    print "\nTesting the data ...............\n"

    submitFile.write("Id"+","+"Sentiment"+"\n")   



    for t , iD in dataTest.iterrows():



        if type(t) == float and np.isnan(t):  # replace empty text to space
            t = " "

        text = gs_clf_svm.predict([t])
        score = str(text)[1:-1]
        submitFile.write(str(iD[" ID"])+","+score+"\n")  




    # missing value

    score="2"
    submitFile.write(str("540")+","+score+"\n")
    submitFile.write(str("5000")+","+score+"\n")  
    submitFile.write(str("6828")+","+score+"\n")  

    submitFile.close()




    print "\nSuccessfully training and testing tha data .\n"
                 





if __name__ == '__main__':


    trainTest()
