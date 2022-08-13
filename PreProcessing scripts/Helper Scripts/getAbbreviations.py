from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import os
import json

dir = '/Users/hadihamoud/Downloads/www/emr/DiagnosesXML/Unannotated'
stopwordsFile = open('/Users/hadihamoud/Desktop/FYPEPIC/DISCO/DISCOBuilder-1.1.1/stopword-lists/stopword-list_en_utf8.txt','r')
stopwords = stopwordsFile.read()
stopwords = stopwords.split('\n')

def tokenizeText(text,dic):
    toktext = word_tokenize(text)
    for word in toktext:
        if len(word)<5 and word not in stopwords:
            if word in dic:
                dic[word]+=1
            else:
                dic[word]=1
        
    

dic = {}
i=0
for filer in os.listdir(dir):
    try:
            print(i,': ',filer)
            with open(os.path.join(dir,filer),'r') as f:
                data = f.read()
            Bs_data = BeautifulSoup(data,'xml')
            
            b_text = Bs_data.find_all('text',text = True)
            for text in b_text:
                tokenizeText(text.text,dic)    
            i+=1     
    except:
            i+=1
            continue

jsondic = json.dumps(dic)

filew = open('AbbreviationsForChadi.txt','w')
with open('AbbreviationsForChadiDICT.txt', 'w') as dictw:
    dictw.write(jsondic)
for word in dic:
    filew.write(str(word)+'\n')
