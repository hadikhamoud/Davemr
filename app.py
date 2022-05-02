from flask import Flask, jsonify
from flask import request
# from flask_cors import CORS
import requests
import time
import json
from jwcrypto import jwt, jwk
import os
import pandas as pd
from cytotest import PandastoCyto
from getTop3Algo import gettextscore
from pprint import pprint



def InitializeDicts(Init):
    for file in os.listdir(Init.algodir):
        try:
            Init.algos[file] = 0
        except:
            continue
    for file in os.listdir(Init.algodir):
        try:
            Init.algos1[file] = []
        except:
            continue

class Initialize:
        def __init__(self,SymptomsBook="3"):
            self.algos = {}
            self.algos1 = {}
            self.inputSofar = ['']
            self.TopNodes = []
            self.CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
            self.BookDirs = [os.path.join(self.CURRENT_DIR, 'algorithms/Symptoms to diagnosis/Modified_graphs'),os.path.join(self.CURRENT_DIR, 'algorithms/The Patient History/Modified_graphs'),os.path.join(self.CURRENT_DIR, 'algorithms/Modified_graphs Combined')]
            self.HashmapFiles = [os.path.join(self.CURRENT_DIR, 'data/AllOut/jsontestemrNoStopWordsAllNotesAndPubmedv2lowerCaseDiluted12_6.txt'),os.path.join(self.CURRENT_DIR, 'data/The Patient History/Book2jsontestemrNoStopWordslowerCasePubmedAndAllNotesDiluted12_6.txt'),os.path.join(self.CURRENT_DIR, 'data/Combined_Books/CombinedjsontestemrNoStopWordsALlNotesAndPubmedTop4Diluted12_6.txt')]
            self.NameFiles = [os.path.join(self.CURRENT_DIR, 'data/excelNameToRealName.txt'),os.path.join(self.CURRENT_DIR, 'data/Book2excelNameToRealName.txt'),os.path.join(self.CURRENT_DIR, 'data/CombinedBooksexcelNameToRealName.txt')]
            self.algodir = self.BookDirs[2]
            self.hashmapCurrentFile = open(self.HashmapFiles[2])
            self.hashmap = json.load(self.hashmapCurrentFile)
            self.NameCurrentFile = open(self.NameFiles[2])
            self.Names = json.load(self.NameCurrentFile)
            InitializeDicts(self)

        def ChangeBook(self,Choice):
            if  Choice == "2" or Choice == "1" or Choice == "3":
                ChoiceInt = int(Choice)
                self.algodir = self.BookDirs[ChoiceInt-1]
                self.hashmapCurrentFile = open(self.HashmapFiles[ChoiceInt-1])
                self.NameCurrentFile = open(self.NameFiles[ChoiceInt-1])
                self.SymptomsBook = Choice
                self.hashmap = json.load(self.hashmapCurrentFile)
                self.Names = json.load(self.NameCurrentFile)
            InitializeDicts(self)

        def ClearDict(self):
            self.algos = dict.fromkeys(self.algos, 0)
            self.algos1 = dict.fromkeys(self.algos1, [])
            self.inputSofar = ['']
            self.TopNodes = []
            InitializeDicts(self)




# with open(os.path.join(CURRENT_DIR, 'data/The Patient History/Book2jsontestemrNoStopWordslowerCasePubmedAndAllNotesDiluted12_6.txt'), 'r') as file:
#     data = json.load(file)
# with open(os.path.join(CURRENT_DIR, 'data/Book2excelNameToRealName.txt'), 'r') as file:
#     Names = json.load(file)

# def clearDict():
#     global algos
#     global algos1
#     global inputSofar
#     algos = dict.fromkeys(algos, 0)
#     algos1 = dict.fromkeys(algos, [])
#     inputSofar = ['']


app = Flask(__name__)
Init = Initialize()

def getAccess():
    clientId = "87d44646-b973-4b6c-bb81-55c255f27fad"
    redirecturi = "http://localhost:3000"
    pemfile = open('privatekey.pem', 'rb')
    privatekey = pemfile.read()
    header = {
        "alg": "RS384",
        "typ": "JWT"
    }
    payload = {
        "sub": clientId,
        "aud": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
        "jti": "f9eaafba-2e49-11ea-8880-5ce0c5aee679",
        "exp": time.time() + 80,
        "iss": clientId,
    }
    Token = jwt.JWT(header=header,
                    claims=payload)
    key = jwk.JWK.from_pem(privatekey, password=None)
    Token.make_signed_token(key)
    SignedToken = Token.serialize()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    fulldata = {'grant_type': 'client_credentials',
                'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
                'client_assertion': SignedToken}
    url = 'https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token'
    response1 = requests.post(url, data=fulldata, headers=headers)
    r1dict = json.loads(response1.text)
    accesstoken = r1dict['access_token']
    authorize = "Bearer " + accesstoken
    return authorize


def requestNote(authorize):
    patient = 'ejJD-7U3OqOcsHTnJnjMrDw3'
    authorizelink = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Binary/" + patient
    headersAccess = {'Authorization': authorize}
    response = requests.get(authorizelink, headers=headersAccess)
    return response.text


@app.route('/getnoteepic', methods=['GET'])
def getnoteepic():
    authorize = getAccess()
    fetchedNote = requestNote(authorize)
    return jsonify({
        "text": fetchedNote
    })


@app.route('/ChangeBook',methods=["POST"])
def ChangeBook():
    Chosen = request.json["Book"]
    Init.ChangeBook(Chosen)
    return jsonify({
        "Book": "Book Changed"
    })


@app.route('/RejectNode',methods = ["GET"])
def RejectNode():
    Init.topNodes.pop()
    return jsonify({
        "topNode": Init.topNodes[-1],
    }) 


@app.route('/Addnote', methods=['POST'])
def Note():
    # getNewWord(request.json["text"],data,algos,algos1)
    Init.inputSofar = gettextscore(Init.algos, Init.hashmap, request.json["text"], Init.algos1,Init.inputSofar)
    print(Init.inputSofar)
    if len(Init.inputSofar)<5:
        return jsonify({
        "elementss": "Stall",
    })
    #Decide on Top Three Algorithms
    alg = dict(sorted(Init.algos.items(), key=lambda item: item[1]))
    keys = list(alg.keys())
    values = list(alg.values())

    for i in range(1,4):
        print(keys[-i], ' : ', values[-i])

    Init.topNodes = []
    NodesSorted = sorted(Init.algos1[keys[-3]], key=lambda item: item[1])
    i=0
    while i<len(NodesSorted) and i<3:
        Init.topNodes.append([Init.Names[keys[-3]],NodesSorted[i][0],NodesSorted[i][1]])
        i+=1
    NodesSorted = sorted(Init.algos1[keys[-2]], key=lambda item: item[1])
    i=0
    while i<len(NodesSorted) and i<3:
        Init.topNodes.append([Init.Names[keys[-2]],NodesSorted[i][0],NodesSorted[i][1]])
        i+=1
    NodesSorted = sorted(Init.algos1[keys[-1]], key=lambda item: item[1])
    i=0
    while i<len(NodesSorted) and i<3:
        Init.topNodes.append([Init.Names[keys[-1]],NodesSorted[i][0],NodesSorted[i][1]])
        i+=1
    


    #topNodes = sorted(topNodes, key = lambda item: item[2],reverse = True)

    algorithmFile = os.path.join(Init.algodir, keys[-1])
    algorithmFile1 = os.path.join(Init.algodir, keys[-2])
    algorithmFile2 = os.path.join(Init.algodir, keys[-3])

    df = pd.read_excel(algorithmFile)
    df1 = pd.read_excel(algorithmFile1)
    df2 = pd.read_excel(algorithmFile2)

    try:
        print(keys[-1], ' : ', NodesSorted[0])
        elements, topNode = PandastoCyto(df, marked=NodesSorted[0][0])
        elements1, topNode1 = PandastoCyto(df1)
        elements2, topNode2 = PandastoCyto(df2)
        # for i,j,k in zip(elements,elements1,elements2):
        #     elements[i].extend(elements1[j])
        #     elements[i].extend(elements2[k])

    except:
        elements, topNode = PandastoCyto(df)
        elements1, topNode1 = PandastoCyto(df1)
        elements2, topNode2 = PandastoCyto(df2)


    pprint(Init.topNodes)
    return jsonify({
        "elementss": elements,
        "Name": Init.Names[keys[-1]],
        "Score":values[-1],
        "Score1":values[-2],
        "Score2":values[-3],
        "elementss1": elements1,
        "Name1": Init.Names[keys[-2]],
        "elementss2": elements2,
        "Name2": Init.Names[keys[-3]],
        "topNode":Init.topNodes[-1]

    })



@app.route('/RestOfNotes',methods=['POST'])
def RestOfNotes():
    alg = dict(sorted(Init.algos.items(), key=lambda item: item[1]))
    keys = list(alg.keys())
    values = list(alg.values())

    for i in range(4,7):
        print(keys[-i], ' : ', values[-i])
    
    algorithmFile = os.path.join(Init.algodir, keys[-4])
    algorithmFile1 = os.path.join(Init.algodir, keys[-5])
    algorithmFile2 = os.path.join(Init.algodir, keys[-6])

    df = pd.read_excel(algorithmFile)
    df1 = pd.read_excel(algorithmFile1)
    df2 = pd.read_excel(algorithmFile2)

    try:
        elements, topNode = PandastoCyto(df)
        elements1, topNode1 = PandastoCyto(df1)
        elements2, topNode2 = PandastoCyto(df2)

    except:
        elements, topNode = PandastoCyto(df)
        elements1, topNode1 = PandastoCyto(df1)
        elements2, topNode2 = PandastoCyto(df2)

    return jsonify({
        "elementss": elements,
        "topNode": topNode,
        "Name": Init.Names[keys[-4]],
        "elementss1": elements1,
        "topNode1": topNode1,
        "Name1": Init.Names[keys[-5]],
        "elementss2": elements2,
        "topNode2": topNode2,
        "Name2": Init.Names[keys[-6]],
        "Score":values[-1],
        "Score1":values[-2],
        "Score2":values[-3],
    })


@app.route('/AddnoteNow', methods=['POST'])
def NoteNow():
    gettextscore(algos, data, request.json["text"], algos1,inputSofar)
    alg = dict(sorted(algos.items(), key=lambda item: item[1]))
    keys = list(alg.keys())
    values = list(alg.values())

    print(keys[-1], ' : ', values[-1])
    print(keys[-2], ' : ', values[-2])
    print(keys[-3], ' : ', values[-3])
    NodesSorted = sorted(algos1[keys[-1]], key=lambda item: item[1], reverse=True)

    df = pd.read_excel(os.path.join(algodir, keys[-1]))
    try:
        print(keys[-1], ' : ', NodesSorted[0])
        elements, topNode = PandastoCyto(df, marked=NodesSorted[0][0])
    except:
        elements, topNode = PandastoCyto(df)

    return jsonify({
        "elementss": elements,
        "topNode": topNode
    })


@app.route('/reset', methods=['POST'])
def reset():
    Init.ClearDict()
    return jsonify({
        "reset": "Reset Successful"
    })

# CORS(app)
