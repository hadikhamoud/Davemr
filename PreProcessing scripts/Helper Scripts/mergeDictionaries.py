import json

def MergeDicts(dic1,dic2):
    for el in dic2:
        if el in dic1:
            for occur in dic2[el]:
                if occur not in dic1[el]:
                    dic1[el].append(occur)

        else:
            dic1[el] = dic2[el]



with open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/Combined_Books/CombinedjsontestemrNoStopWordsALlNotesTop4.txt','r') as file:
    dic1 = json.load(file)

with open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/Combined_Books/CombinedjsontestemrNoStopWordsPubmedTop4.txt','r') as file:
    dic2 = json.load(file)

MergeDicts(dic1,dic2)

dic1.update(dic2)

with open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/Combined_Books/CombinedjsontestemrNoStopWordsALlNotesAndPubmedTop4.txt', 'w') as convert_file:
     convert_file.write(json.dumps(dic1))
convert_file.close()

        
