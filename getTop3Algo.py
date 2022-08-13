import nltk
from spellchecker import SpellChecker
import json
import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


#get medical terms and medical abbreviations and load them into dictionary
MedicalFileR = open(os.path.join(CURRENT_DIR,'data/MedicalAbbr/MedicalTermsDict.txt'),'r')
AbbreviationsFileR = open(os.path.join(CURRENT_DIR,'data/MedicalAbbr/AbbreviationsOnly.txt'),'r')
MedD = json.load(MedicalFileR)
AbbrD = json.load(AbbreviationsFileR)

#spell check the given words
def SpellCheckerWithUnknown(word,AbbrD,MedD):
    spell = SpellChecker()

    #using spellChecker, if word is unknown then it might be a spelling mistake or a medical term
    misspelled = spell.unknown([word.lower()])
    if len(misspelled)!=0:
        #check misspelled word and check if it exists in the medical words and the abbreviations dataset
        misspelled_word = misspelled.pop()
        if misspelled_word not in AbbrD and misspelled_word not in MedD:
            #if does not exist, try to correct
           return spell.correction(word)
        else:
            return word
    else:
        return word




#use the negation list to deny successors to negation words
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

#ADD THE newly added input to scoring
def addScore(algoScore,algoNodeScore,x):
    #check if the word exists (is found) in the word map
    #add the score to the algoScore key for all algorithm matches
    #  and add the node scores for each algorithm progressively into algoNodeScore 
    #increment the score given the algorithms
    for y in x:
        algoScore[y[0]] = algoScore[y[0]] + y[2]
        z = algoNodeScore[y[0]]
        found = False
        for i in range(0, len(z)):
            if y[1] == z[i][0]:
                algoNodeScore[y[0]][i][1] = algoNodeScore[y[0]][i][1] + y[2]
                found = True

        if (found):
            found = False
        else:
            algoNodeScore[y[0]].append([y[1], y[2]])


#substract the deleted input from scorin
#same process but substact from score if word is found
def subScore(algoScore,algoNodeScore,x):
        for y in x:
            algoScore[y[0]] = algoScore[y[0]] - y[2]
            z = algoNodeScore[y[0]]
            found = False
            for i in range(0, len(z)):
                if y[1] == z[i][0]:
                    algoNodeScore[y[0]][i][1] = algoNodeScore[y[0]][i][1] - y[2]
                    found = True



#compare new input with older state input dynamically to adjust algorithm scores
def wordsofcomparison(oldinput,newinput):
    nO = len(oldinput)
    nN = len(newinput)
    outputTemp = []
    outputAdd =[]
    outputSub = []
    oldTemp = oldinput.copy()
    newTemp = newinput.copy()

    if nO<=nN:
        #oldTemp and newTemp represent the sentences before adding the new words and after it respectively
        #add FILLER_VALUE to keep consistency of both arrays and compare for changes
        #extra words are added in scoring and changed words modify the scoring
        #deleted words substract from score
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
    #return what to add for scoring and what to substract from score
    return outputAdd,outputSub



                


#combine previously mentioned functions to score input dynamically
def gettextscore(algoScore, data, inputofuser, algoNodeScore,previnput):
    tokenizedinput = nltk.word_tokenize(inputofuser)
    tokenizedinput = [word.lower() for word in tokenizedinput]
    Add,Sub = wordsofcomparison(previnput,tokenizedinput)

    n = len(Add)

    if len(previnput)>=1 and previnput[-1] in negation_list:
        #mark word with negexdel to delete the word from scoring (only in dynamic scoring)
        Add[0] = "negexdel"
    
    #spell check the addition and substraction arrays and modify
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

    #add words to score using addScore helper function
    for word in Add:
        if word in data:
            x = data[word]
            addScore(algoScore,algoNodeScore,x)

    #substract words from score using subScore helper function
    for word in Sub:
        if word in data:
            x = data[word]
            subScore(algoScore,algoNodeScore,x)
    
    return tokenizedinput
    

            
    

