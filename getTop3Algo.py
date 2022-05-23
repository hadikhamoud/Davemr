import nltk
from spellchecker import SpellChecker
import json
import os

nltk.download('punkt')
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

MedicalFileR = open(os.path.join(CURRENT_DIR,'data/MedicalAbbr/MedicalTermsDict.txt'),'r')
AbbreviationsFileR = open(os.path.join(CURRENT_DIR,'data/MedicalAbbr/AbbreviationsOnly.txt'),'r')
MedD = json.load(MedicalFileR)
AbbrD = json.load(AbbreviationsFileR)


def SpellCheckerWithUnknown(word,AbbrD,MedD):
    spell = SpellChecker()

    misspelled = spell.unknown([word.lower()])
    if len(misspelled)!=0:
        misspelled_word = misspelled.pop()
        if misspelled_word not in AbbrD and misspelled_word not in MedD:
           return spell.correction(word)
        else:
            return word
    else:
        return word





negation_list = ['denies', 'evaluate for', 'no signs of', 'no', "doesn't", 'cannot', 'rules out', 'without signs of',
                 'no complaints of', 'rule out', 'ruled the patient out', 'symptoms atypical', 'no sign of', '-', 'fails to reveal',
                 'denied', 'doesnt', 'didnt', 'rule the patient out', ' -', 'rule him out', 'dont', 'werent', "can't", 'no cause of',
                 'rule her out', 'absence of', "isn't", 'couldnt', 'declined', 'never', 'never had', 'not', 'isnt', 'cant',
                 'without sign of', 'never developed', "didn't", 'free of', 'ruled her out', 'rule patient out',
                 'without any reactions or signs of', 'ruled patient out', 'without', 'denying',
                 'doubt', "aren't", 'patient was not', 'r/o', "weren't", 'did not exhibit', 'negative for',
                 "don't", 'arent', 'without indication of', "couldn't", 'wasnt', "wasn't", 'ruled out', 'versus', 'ro',
                 'not demonstrate', 'ruled him out', 'no evidence of']

negation_list = set(negation_list)

def getNewWord(inputofuser, data, algos, algos1):
    tokenizedword = nltk.word_tokenize(inputofuser)
    word = tokenizedword[-1]
    getwordscore(algos, data, word, algos1)


# for continous visualization
def getwordscore(algos, data, word, algos1):
    try:
        x = data[word]
        for y in x:
            algos[y[0]] = algos[y[0]] + y[2]
            z = algos1[y[0]]
            found = False
            for i in range(0, len(z)):
                if y[1] == z[i][0]:
                    algos1[y[0]][i][1] = algos1[y[0]][i][1] + y[2]
                    found = True

            if (found):
                found = False
            else:
                algos1[y[0]].append([y[1], y[2]])

    except:
        return


def addScore(algos,algos1,x):
    for y in x:
        algos[y[0]] = algos[y[0]] + y[2]
        z = algos1[y[0]]
        found = False
        for i in range(0, len(z)):
            if y[1] == z[i][0]:
                algos1[y[0]][i][1] = algos1[y[0]][i][1] + y[2]
                found = True

        if (found):
            found = False
        else:
            algos1[y[0]].append([y[1], y[2]])

def subScore(algos,algos1,x):
        for y in x:
            algos[y[0]] = algos[y[0]] - y[2]
            z = algos1[y[0]]
            found = False
            for i in range(0, len(z)):
                if y[1] == z[i][0]:
                    algos1[y[0]][i][1] = algos1[y[0]][i][1] - y[2]
                    found = True




def wordsofcomparison(oldinput,newinput):
    nO = len(oldinput)
    nN = len(newinput)
    outputTemp = []
    outputAdd =[]
    outputSub = []
    oldTemp = oldinput.copy()
    newTemp = newinput.copy()

    if nO<=nN:
        oldTemp.extend('FILLER_VALUE' for i in range(nN-nO+1))
        for i, (first,second) in enumerate(zip(oldTemp,newTemp)):                
            if first!=second:
                outputTemp.append((i,second))
        for tup in outputTemp:
            idx = tup[0]
            word = tup[1]
            if oldTemp[idx]!='FILLER_VALUE':
                outputSub.append(oldTemp[idx])
            outputAdd.append(word)
    else:
        newTemp.extend('FILLER_VALUE' for i in range(nO-nN+1))
        for i, (first,second) in enumerate(zip(newTemp,oldTemp)):
            if first!=second:
                outputTemp.append((i,second))
        for tup in outputTemp:
            idx = tup[0]
            word = tup[1]
            if newTemp[idx]!='FILLER_VALUE':
                outputAdd.append(newTemp[idx])
            outputSub.append(word)
    return outputAdd,outputSub



                



def gettextscore(algos, data, inputofuser, algos1,previnput):
    tokenizedinput = nltk.word_tokenize(inputofuser)
    tokenizedinput = [word.lower() for word in tokenizedinput]
    Add,Sub = wordsofcomparison(previnput,tokenizedinput)

    n = len(Add)

    if len(previnput)>=1 and previnput[-1] in negation_list:
        Add[0] = "negexdel"
    
        

    for i in range(n):
        if Add[i] in negation_list:
            Add[i] = "negex"
            if i!=n-1:
                Add[i+1]="negexdel"
        if Add[i] not in data:
            Add[i] = SpellCheckerWithUnknown(Add[i],AbbrD,MedD)
    for i in range(len(Sub)):
        if Sub[i] not in data:
             Sub[i] = SpellCheckerWithUnknown(Sub[i],AbbrD,MedD)
    print("Add: ",Add)
    print("Sub: ",Sub)
    for word in Add:
        if word in data:
            x = data[word]
            addScore(algos,algos1,x)
    for word in Sub:
        if word in data:
            x = data[word]
            subScore(algos,algos1,x)
    
    return tokenizedinput
    

            
    




def getTop3Algo(algos):
    n1 = ["", 0]
    n2 = ["", 0]
    n3 = ["", 0]
    for x in algos:
        if algos[x] > n1[1]:
            n1[0] = x
            n1[1] = algos[x]
        elif algos[x] > n2[1]:
            n2[0] = x
            n2[1] = algos[x]
        elif algos[x] > n3[1]:
            n3[0] = x
            n3[1] = algos[x]
    return n1

    # print("")
    # print("TOP 3 MATCHS:")
    # print(n1)
    # print(n2)
    # print(n3)


# def gettextscore(algos, data, inputofuser, algos1,previnput):
#     tokenizedinput = nltk.word_tokenize(inputofuser)
#     previnput = nltk.word_tokenize(inputofuser)
#     Add,Sub = wordsofcomparison(previnput,tokenizedinput)
    
#     n = len(tokenizedinput)
#     for i in range(n-1):
#          if tokenizedinput[i]=='NEGEX':
#                 continue
#          if tokenizedinput[i] in negation_list:
#                 tokenizedinput[i+1] = 'NEGEX'
#                 continue
#          if tokenizedinput[i] not in data:
#              tokenizedinput[i] = SpellCheckerWithUnknown(tokenizedinput[i],AbbrD,MedD)
#     for i in range(n-1):
#         if tokenizedinput[i] in data:
#             x = data[tokenizedinput[i]]
#             addScore(algos,algos1,x)
    
#     if n<5:
#         return "Stall"
            
#     return inputofuser