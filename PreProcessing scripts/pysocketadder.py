import socket
import json
import copy



HOST = "localhost"
PORT = 807
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

JSON_dict = '/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/Combined_Books/CombinedjsontestemrNoStopWords.txt'
f = open(JSON_dict,'r')
BigData = json.load(f)
BigDataIn = copy.deepcopy(BigData)

def JavaToDict(data):

    dat = data.replace('\n','|')
    dat = dat.split('|')
    dic = {}
    for i in range(0,len(dat)-2,2):
        dic[dat[i]] = float(dat[i+1])/10000
    return dic

def AddScores(Scores,discowords):
    
    tempDict = {}
    for word in discowords:
        tempDict[word]=[]
        for score in Scores:
            temp = copy.deepcopy(score)
            tempDict[word].append(temp)
            tempDict[word][-1][2] = discowords[word]

        
    return tempDict

def AddtoMainDict(BigDict,Dict):
    for word in Dict:
        if word in BigDict:
            for w in Dict[word]:
                BigDict[word].append(w)
        else:
            BigDict[word]=Dict[word]



run = True
while run:
    for key in BigDataIn:
        n = key
        n+='\n'
        bn = bytes(n,'utf-8')
        sock.sendall(bn)
        data = sock.recv(1024)
        if not data:
            sock.shutdown(socket.SHUT_RDWR)
            break
        discowords = JavaToDict(data.decode('utf-8'))
        if len(discowords)==0:
            continue
        Scores = copy.deepcopy(BigDataIn[key])
        tempDict = AddScores(Scores,discowords)
        AddtoMainDict(BigData,tempDict)
        if n =='endER\n':
            sock.close()
        data =b''
    with open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/Combined_Books/CombinedjsontestemrNoStopWordsPubmedTop4.txt', 'w') as convert_file:
     convert_file.write(json.dumps(BigData))
    convert_file.close()
    break
        
        


 

