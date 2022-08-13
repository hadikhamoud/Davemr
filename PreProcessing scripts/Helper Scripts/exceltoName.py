import os
import json

dic = {}

CURRENT_DIR = "/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/algorithms/The Patient History"

for file in os.listdir(CURRENT_DIR):
    print("Name for This: ",file)
    dic[file] = input('input: ')


jsondic = json.dumps(dic)

f = open('Book2excelNameToRealName.txt','w')
f.write(jsondic)
f.close()
    
