import pandas as pd
import nltk
import os
import json

def findInKey(L,id):
    for i in L:
        if id in i:
            return True
    return False


def intoD(df,D,file):
    nodes = df['Unnamed: 1']
    ids = df['Nodes']

    for (node,id) in zip(nodes,ids):
        try:
            tokenized = nltk.word_tokenize(node)
            tokenized = [word.lower() for word in tokenized]
            for word in tokenized:
                if word not in D:
                    D[word] = [[file,int(id),1]]
                else:
                    if not findInKey(D[word],id):
                        D[word].append([file,int(id),1])
                    
        except:
            continue

    return "done with "+file
    


dir = "/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/algorithms/Combined Books"



D = {}
i=0
for file in os.listdir(dir):
    
    try:
        df = pd.read_excel(os.path.join(dir,file))
        print(intoD(df,D,file))
        i+=1
    except:
        continue

with open("/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/Combined_Books/Combinedjsontestemr.txt", 'w') as convert_file:
     convert_file.write(json.dumps(D))
print(i," files")
print(len(D))
    
convert_file.close()







