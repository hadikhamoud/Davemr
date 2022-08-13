import pandas as pd
import os

def getGraphLevels(df,levels=0):
    df = df.iloc[1: , :]
    dicT=[]
    ranks={}
    for t in df['Unnamed: 7']:
        dicT.append(t)

    i = 1
    prev = 0
    
    while len(dicT)!=prev:
        prev = len(dicT)
        ranks[i]=[]
        temp = []
        indices=[]
        for index, row in df.iterrows():
            if row['Edges'] not in dicT:
                ranks[i].append(row['Edges'])
                temp.append(row['Unnamed: 7'])
                indices.append(index)
        for nodes in temp:
            dicT.remove(nodes)
        for ind in indices:
            df.drop(labels = ind,inplace = True)
        ranks[i] = set(ranks[i])
        i+=1
    return ranks


def addLevels(df):
    ranks = []
    foundRank = False
    levels = getGraphLevels(df)
    df = df.iloc[1: , :]
    for el in df["Nodes"]:
        for rank in levels:
            if el in levels[rank]:
                ranks.append(rank)
                foundRank = True
        if not foundRank:
            ranks.append(0)
        foundRank=False
    ranks.insert(0,0)
    return ranks


# DIR = "/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/algorithms/The Patient History"
# MODIFIED_DIR = DIR+'/Modified_graphs'

file = '/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/algorithms/Modified_graphs Combined/ch 10-3 diagnostic approach.xlsx'

# for file in os.listdir(DIR):
#         try:
#             df = pd.read_excel(os.path.join(DIR,file))
#             ranks = addLevels(df)
#             if len(ranks)<len(df):
#                 ranks.extend(0 for i in range(len(df)-len(ranks)))
#             df["Ranks"] = ranks
#             df.to_excel(os.path.join(MODIFIED_DIR,file[:-5]+".xlsx"),index=False)
#         except:
#             continue



df = pd.read_excel(file)
ranks = addLevels(df)
if len(ranks)<len(df):
    ranks.extend(0 for i in range(len(df)-len(ranks)))
df["Ranks"] = ranks
df.to_excel(file,index=False)




        
    
