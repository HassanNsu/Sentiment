#!/usr/bin/python
# -*- coding: utf-8 -*-
from textblob import TextBlob
import exceptions
import appos
import re
import pandas as pd



def preprocessing():

#------------------------------------------- clean the text from trainfile_r3.csv........................

    print "\nCleaning the text from trainfile_r3.csv................\n"

    cleanTextFile_train = open("cleanTextFile_train.csv", "a+")
    originalData_train = pd.read_csv("trainfile_r3.csv",index_col=0, encoding='utf-8-sig')


    cleanTextFile_train.write("Text"+", "+"Sentiment"+"\n")   
    
    for text, sentiment in originalData_train.iterrows():

        lengthText = findLength(text,cleanTextFile_train,sentiment["Sentiment"])

        if lengthText==-1:
            continue


        
        if lengthText < 3:                                                              # detect the length of text less than three for textblob, because textBlob throw exception for small text
            checkLength(text,cleanTextFile_train,sentiment["Sentiment"])
            continue  
        text2 = removeCarriage(text)


        trans= translateTextToEnglish(text2,cleanTextFile_train,sentiment["Sentiment"])  # Translate all the text to English

        if(trans==-1):
            continue
        else:
            cleanTextFile_train.write(str(trans)+", "+str(sentiment["Sentiment"])+"\n")    

    cleanTextFile_train.close()

# ----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------




#------------------------------------------- clean the text from testfile_r3.csv....................................


    print "\nCleaning the text from testfile_r3.csv................\n"

    cleanTextFile_test = open("cleanTextFile_test.csv", "a+")
    originalData_test = pd.read_csv("testfile_r3.csv",index_col=0, encoding='utf-8-sig')


    cleanTextFile_test.write("Text"+", "+"ID"+"\n")   
    
    for id , text in originalData_test.iterrows():

        lengthText = findLength(text["Text"],cleanTextFile_test,id)

        if lengthText==-1:
            continue


        
        if lengthText < 3:
            checkLength(text["Text"],cleanTextFile_test,id)
            continue  
        text2 = removeCarriage(text["Text"])


        trans= translateTextToEnglish(text2,cleanTextFile_test,id)

        if(trans==-1):
            continue
        else:
            cleanTextFile_test.write(str(trans)+", "+str(id)+"\n")

    cleanTextFile_test.close()

    print "\nSuccessfully clean both train and test file\n"
    

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------            

def translateTextToEnglish(txt,cleanFile,senti):

    b = TextBlob(txt)
    ch = str(b.detect_language())
    if(ch!='en' and ch!='bn'):  # translate Romanized Bangla to English
            
        try:
            trans2=  b.translate(to='bn')
        except Exception :

            r= cleanText(b)
            cleanFile.write(str(r)+", "+str(senti)+"\n")                
            return -1

        try:
            trans= trans2.translate(to='en')
        except Exception :

            r= cleanText(b)
            cleanFile.write(str(r)+", "+str(senti)+"\n")                   

            return -1

        r= cleanText(trans)

        return r          

            

    elif(ch=='bn'):                      # translate Bangla to English
        trans=  b.translate(to='en')
        r= cleanText(trans)

        return r

            

    else:
        trans=b
        r= cleanText(trans)

        return r






def removeCarriage(txt):

    words = txt.split()
    ans = ""
    for w in words:
        w = w.replace("\\r\\n", " ")   # remove newline from text
        ans = ans + w +" "

    return ans


def checkLength(txt,cleanFile,senti):

    text = txt.encode('utf-8')
    cleanFile.write(str(text)+", "+str(senti)+"\n")



def findLength(txt,cleanFile,senti):

    try:
        length = len(txt)
        return length
    except Exception:
        cleanFile.write(str(txt)+", "+str(senti)+"\n")  
        return -1


def cleanText(txt):

    s = str(txt)

    commaFreetext = s.replace(',', ' ')       #replace comma with space

    removeRepChar = re.sub(r'(.)\1{3,}', r'\1\1', commaFreetext)  # Remove repeated character

    createSpacePunc = re.sub(r'([\.\?\!\;\:\-\_\(\)\{\}\[\]\"\<\>\/\@\#\&])\1*', r' \1 ', removeRepChar)    # separate punctuation for every word


    words = createSpacePunc.split()
    reformed = [appos.appos[word] if word in appos.appos else word for word in words]   # transform appostrophe to full sentence like don't to do not


    joinWord = ""
    for w in reformed:
        joinWord = joinWord + w +" "

    return joinWord


if __name__ == '__main__':


    preprocessing()
