from flask import Flask, jsonify, send_from_directory
from flask import request
from flask_cors import CORS
import requests
import time
import json
from jwcrypto import jwt, jwk
import os
import pandas as pd
from cytotest import PandastoCyto
from getTop3Algo import gettextscore
from pprint import pprint
from flask_talisman import Talisman



#Helper functions for Initialization class and graph scoring

#function to get the GRAPH elements for cytoscape
def getGraph(JSONcyto,graphname):
    if graphname in JSONcyto:
        return JSONcyto[graphname]
    else:
        print(f'{graphname} does not exist')
        return None

def InitializeDicts(Init):
    for file in os.listdir(Init.algodir):
        try:
            Init.algoScore[file] = 0
        except:
            continue
    for file in os.listdir(Init.algodir):
        try:
            Init.algoNodeScore[file] = []
        except:
            continue



class Initialize:
        def __init__(self,SymptomsBook="3"):
            #dictionary containing each algorithm graph coupled with its score in real time
            self.algoScore = {}

            #dictionary scoring each node in each algorithm in order to determine the top node of the algorithm graph
            self.algoNodeScore = {}

            #user's input tokenized in list
            self.inputSofar = ['']

            #current directory to retrieve model and other useful files
            self.CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

            #load graph elements into graphs variable
            self.graphs = json.load(open(os.path.join(self.CURRENT_DIR,'data/JSONGraphs.txt')))

            #load books
            self.BookDirs = [os.path.join(self.CURRENT_DIR, 'algorithms/Symptoms to diagnosis/Modified_graphs'),os.path.join(self.CURRENT_DIR, 'algorithms/The Patient History/Modified_graphs'),os.path.join(self.CURRENT_DIR, 'algorithms/Modified_graphs Combined')]

            self.HashmapFiles = [os.path.join(self.CURRENT_DIR, 'data/Symptoms To Diagnosis/SymptomsToDiagJson.txt'),os.path.join(self.CURRENT_DIR, 'data/The Patient History/PatientHistoryJson.txt'),os.path.join(self.CURRENT_DIR, 'data/Combined_Books/CombinedBooksJsonFinal.txt')]

            #load graph names for better user experience
            self.NameFiles = [os.path.join(self.CURRENT_DIR, 'data/excelNameToRealName.txt'),os.path.join(self.CURRENT_DIR, 'data/Book2excelNameToRealName.txt'),os.path.join(self.CURRENT_DIR, 'data/CombinedBooksexcelNameToRealName.txt')]
            self.algodir = self.BookDirs[2]
            self.hashmapCurrentFile = open(self.HashmapFiles[2])
            self.hashmap = json.load(self.hashmapCurrentFile)
            self.NameCurrentFile = open(self.NameFiles[2])
            self.Names = json.load(self.NameCurrentFile)
            InitializeDicts(self)

        
        def ChangeBook(self,Choice):
            #Choose between book1, book2, or both books combined
            if Choice == "1" or Choice == "2"  or Choice == "3":
                ChoiceInt = int(Choice)
                self.algodir = self.BookDirs[ChoiceInt-1]
                self.hashmapCurrentFile = open(self.HashmapFiles[ChoiceInt-1])
                self.NameCurrentFile = open(self.NameFiles[ChoiceInt-1])
                self.SymptomsBook = Choice
                self.hashmap = json.load(self.hashmapCurrentFile)
                self.Names = json.load(self.NameCurrentFile)
            InitializeDicts(self)
        
        #clear all elements in dictionary
        def ClearDict(self):
            self.algoScore = dict.fromkeys(self.algoScore, 0)
            self.algoNodeScore = dict.fromkeys(self.algoNodeScore, [])
            self.inputSofar = ['']
            self.TopNodes = []
            InitializeDicts(self)




#initializing FLASK variables
app = Flask(__name__, static_url_path='', static_folder='Dave-frontend/buildMe')
Init = Initialize()


#for development, we use flask_cors, and for production on Heroku, we use
#flask Talisman to enforce https on the app level

CORS(app)
#Talisman(app, content_security_policy=None)



#EPIC SANDBOX ACCESS Testing
#Replace clientId and jti with appropriate values(refer to EPIC EHR documentations)

def getAccess():
    clientId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
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
        "jti":  "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
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

#Example request note for example sandbox patient
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






#change the given book
@app.route('/ChangeBook',methods=["POST"])
def ChangeBook():
    Chosen = request.json["Book"]
    Init.ChangeBook(Chosen)
    return jsonify({
        "Book": "Book Changed"
    })




@app.route('/Addnote', methods=['POST'])
def Note():
    Init.inputSofar = gettextscore(Init.algoScore, Init.hashmap, request.json["text"], Init.algoNodeScore,Init.inputSofar)
    print(Init.inputSofar)
    if len(Init.inputSofar)<5:
        return jsonify({
        "elementsG1": "Stall",
    })
    #Decide on Top Three Algorithms
    #sort them by algorithm score
    alg = dict(sorted(Init.algoScore.items(), key=lambda item: item[1]))
    keys = list(alg.keys())
    values = list(alg.values())

    for i in range(1,4):
        print(keys[-i], ' : ', values[-i])
   
   #get the top three scoring algorithms
   #use the getGraph function mentioned above to retrieve the graph elements in order to send
    elementsG1 = getGraph(Init.graphs,keys[-1])
    elementsG2 = getGraph(Init.graphs,keys[-2])
    elementsG3 = getGraph(Init.graphs,keys[-3])

    #send the graph name, the graph elements and the graph scores
    return jsonify({
        "elementsG1": elementsG1,
        "elementsG2": elementsG2,
        "elementsG3": elementsG3,
        "NameG1": Init.Names[keys[-1]],
        "NameG3": Init.Names[keys[-3]],
        "NameG2": Init.Names[keys[-2]],
        "ScoreG1":round(values[-1],2),
        "ScoreG2":round(values[-2],2),
        "ScoreG3":round(values[-3],2),

        })






#same approach as above but for 4,5, and 6th graphs
@app.route('/RestOfNotes',methods=['POST'])
def RestOfNotes():
    alg = dict(sorted(Init.algoScore.items(), key=lambda item: item[1]))
    keys = list(alg.keys())
    values = list(alg.values())

    for i in range(4,7):
        print(keys[-i], ' : ', values[-i])
    
    elementsG4 = getGraph(Init.graphs,keys[-1])
    elementsG5 = getGraph(Init.graphs,keys[-2])
    elementsG6 = getGraph(Init.graphs,keys[-3])

    return jsonify({
        "elementsG4": elementsG4,   
        "elementsG5": elementsG5, 
        "elementsG6": elementsG6,
        "NameG4": Init.Names[keys[-4]],
        "NameG5": Init.Names[keys[-5]],
        "NameG6": Init.Names[keys[-6]],
        "ScoreG4":round(values[-4],-2),
        "ScoreG5":round(values[-5],2),
        "ScoreG6":round(values[-6],2),
     })








#reset all elements for scoring
@app.route('/reset', methods=['POST'])
def reset():
    Init.ClearDict()
    return jsonify({
        "reset": "Reset Successful"
    })





#serve main page
@app.route('/')
def serve():
    return send_from_directory(app.static_folder,'index.html')







if __name__ == "__main__": 
     app.run(host = '0.0.0.0',debug=False, port=os.environ.get('PORT', 5000))


