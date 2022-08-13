import json
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
filer = os.path.join(CURRENT_DIR,'AllOut/jsontestemrNoStopWordsAllNotesAndPubmedv2lowerCase.txt')
f = open(filer,'r')
#----------------------------------------StopWords
data = f.read()

stopwordsFile = open('/Users/hadihamoud/Desktop/FYPEPIC/DISCO/DISCOBuilder-1.1.1/stopword-lists/stopword-list_en_utf8.txt','r')

stopwords = stopwordsFile.read()

stopwords = stopwords.split('\n')



datar = json.loads(data)

dataw = datar.copy()

for i in datar:
    if i in stopwords:
        dataw.pop(i)

#----------------------------high frequency

def DiluteFrequencyWords(dic,high,mid):
    change = 1
    for words in dic:
        occur = len(dic[words])
        if occur>=high:
            change = 0.2
        elif occur>=mid and occur<high:
            change = 0.5
        
        if change!=1:
            for occ in dic[words]:
                if(occ[2]==1):
                    occ[2]=change



        
DiluteFrequencyWords(dataw,12,6)
    
alg = dict(sorted(datar.items(), key=lambda item: len(item),reverse=True))
keys = list(alg.keys())
values = list(alg.values())

print(keys[0],values[0])

jsonDict = json.dumps(dataw)


filew = filer+'Diluted12_6.txt'

with open(filew, 'w') as convert_file:
    convert_file.write(jsonDict)

convert_file.close()

