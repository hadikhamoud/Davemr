
import json
import os
import sys
sys.path.append('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server')
from cytotest import PandastoCyto
import pandas as pd
import lxml


Book1dir= "/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/algorithms/Symptoms to diagnosis/Modified_graphs"
Book2dir= "/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/algorithms/The Patient History/Modified_graphs" 
BookCombinedir= "/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/algorithms/Modified_graphs Combined"

def pandastocytotoJSON(dir):
    content = os.listdir(dir)
    outputJSON = {}
    for graph in content:
        try:
            df = pd.read_excel(os.path.join(dir,graph))
            outputCyto = PandastoCyto(df)
            outputJSON[graph] = outputCyto
        except:
            continue
      
    
    return outputJSON

def mergeDicts(dic1,dic2):
    for el in dic2:
        if el in dic1:
            print("found common element: ",el)
        else:
            dic1[el] = dic2[el]


Book1dic = pandastocytotoJSON(Book1dir)
Book2dic = pandastocytotoJSON(Book2dir)

mergeDicts(Book1dic,Book2dic)

print(len(Book1dic))

JSONgraphs= open("/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/JSONGraphs.txt",'w')

JSONgraphs.write(json.dumps(Book1dic))




