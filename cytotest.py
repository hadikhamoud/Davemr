
import pandas as pd



COLORS = {
    'beige':'#f5f5dc',
    'teal':'#008080',
    'purple':'#CBC3E3',
    'orange':'#FFA500',
    'light orange':'#FFD580',
    'blue':'#ADD8E6',
}

SHAPE = {
    'test':'round-rectangle',
    '':'',
}

def getGraphLevels(df,levels):
    df = df.iloc[1: , :]
    dicT=[]
    ranks={}
    for t in df['Unnamed: 7']:
        dicT.append(t)


    
    for i in range(1,levels+1):
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
    return ranks


def PandastoCyto(df,index='A',marked=1):
    x=1
    topNode = '[id = "'+ index+str(marked)+'"]'
    elements = {
        'nodes':[],
        'edges':[]
    }
    #level3 = getGraphLevels(df,3)
   
    for (i,c,shape,col,rank) in zip(df['Nodes'],df['Unnamed: 1'],df['Unnamed: 2'],df['Unnamed: 3'],df['Ranks']):
        try:
            label =str(c)
            prefcolor = COLORS.get(col)
            prefshape = SHAPE.get(shape)
            if prefshape==None:
                prefshape="round-rectangle"
            if prefcolor==None:
                prefcolor = COLORS.get('beige')

            elements['nodes'].append({'data': {'id': index+str(int(i)), 'label': label,'type':'data','group':index,'prefcolor':prefcolor,'prefshape':prefshape,'rank':str(rank),'TopNode':'0'}})
            # elements['nodes'].append({'data': {'id': index+str(int(i))+"YES", 'label': 'YES','type':'YES/NO'}})
            # elements['nodes'].append({'data': {'id': index+str(int(i))+"NO", 'label': 'NO','type':'YES/NO'}})


        except ValueError:
            continue

    for (s, t, l) in zip(df['Edges'], df['Unnamed: 7'], df['Unnamed: 8']):
        try:
            label = str(l)
            if label == 'nan':
                label = ''
            elements['edges'].append({'data': {'source': index+str(int(s)),'target':index+str(int(t)),'label': label}})
            # elements['edges'].append({'data': {'source': index+str(int(s)),'target':index+str(int(s))+'YES','group':'YES/NO'}})
            # elements['edges'].append({'data': {'source': index+str(int(s)),'target':index+str(int(s))+'NO','group':'YES/NO'}})

        except ValueError:
            continue

    return elements,topNode



def MergePandasToCyto(df,df2,A,B,C):
    elements = {
        'nodes': [],
        'edges': []
    }

    elements1 = PandastoCyto(df)
    elements2 = PandastoCyto(df2,"B")

    elements['nodes'].append({'data': {'id': C, 'label': 'COMMON NODE!'}})

    for edge in elements1['edges']:
        if edge['data']['source'] == A:
            edge['data']['source'] = C

        if edge['data']['target'] == A:
            edge['data']['target'] = C

        elements['edges'].append(edge)

    for edge in elements2['edges']:
        if edge['data']['source'] == B:
            edge['data']['source'] = C

        if edge['data']['target'] == B:
            edge['data']['target'] = C

        elements['edges'].append(edge)

    for x in elements1['nodes']:
        elements['nodes'].append(x)

    for x in elements2['nodes']:
        elements['nodes'].append(x)


    return elements

