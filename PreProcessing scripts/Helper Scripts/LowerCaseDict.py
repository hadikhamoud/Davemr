import os
import json

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
f = open(os.path.join(CURRENT_DIR,'The Patient History/Book2jsontestemrNoStopWordsPubmed.txt'),'r')
data = f.read()
datar = json.loads(data)
dataw={}

for k in datar:
    tempK = k.lower()
    if tempK not in dataw:
        dataw[tempK] = datar[k]
    else:
        dataw[tempK].extend(datar[k])



jsonDict = json.dumps(dataw)

filew = os.path.join(CURRENT_DIR,'The Patient History/Book2jsontestemrNoStopWordsPubmed')+'lowerCase.txt'
with open(filew, 'w') as convert_file:
    convert_file.write(jsonDict)
convert_file.close()


