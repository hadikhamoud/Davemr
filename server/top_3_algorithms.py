import nltk
from spellchecker import SpellChecker
import json
import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


#get medical terms and medical abbreviations and load them into dictionary
medical_file = open(os.path.join(CURRENT_DIR,'data/medical_terms.json'),'r')
MEDICAL_TERMS = json.load(medical_file)

negation_list_file = open(os.path.join(CURRENT_DIR,'data/negation_list.txt'),'r')
NEGATION_LIST = negation_list_file.read().splitlines()


abbreviations_file = open(os.path.join(CURRENT_DIR,'data/abbreviations.json'),'r')
ABBREVIATIONS = json.load(abbreviations_file)

#spell check the given words
def SpellCheckerWithUnknown(word,ABBREVIATIONS,MEDICAL_TERMS):
    spell = SpellChecker()

    misspelled = spell.unknown([word.lower()])
    if len(misspelled)!=0:
        misspelled_word = misspelled.pop()
        if misspelled_word not in ABBREVIATIONS and misspelled_word not in MEDICAL_TERMS:
           return spell.correction(word)
        else:
            return word
    else:
        return word




#use the negation list to deny successors to negation words


#add THE newly added input to scoring
def addScore(algorithm_scoring,algorithm_node_scoring,x):
    for y in x:
        algorithm_scoring[y[0]] = algorithm_scoring[y[0]] + y[2]
        z = algorithm_node_scoring[y[0]]
        found = False
        for i in range(0, len(z)):
            if y[1] == z[i][0]:
                algorithm_node_scoring[y[0]][i][1] = algorithm_node_scoring[y[0]][i][1] + y[2]
                found = True

        if (found):
            found = False
        else:
            algorithm_node_scoring[y[0]].append([y[1], y[2]])
#substract the deleted input from scoring
def subScore(algorithm_scoring,algorithm_node_scoring,x):
        for y in x:
            algorithm_scoring[y[0]] = algorithm_scoring[y[0]] - y[2]
            z = algorithm_node_scoring[y[0]]
            found = False
            for i in range(0, len(z)):
                if y[1] == z[i][0]:
                    algorithm_node_scoring[y[0]][i][1] = algorithm_node_scoring[y[0]][i][1] - y[2]
                    found = True



#compare new input with older state input dynamically
def words_of_comparison(oldinput,newinput):
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



                


#combine previously mentioned functions to score input dynamically
def get_text_score(algorithm_scoring, data, input_of_user, algorithm_node_scoring,prev_input):
    tokenized_input = nltk.word_tokenize(input_of_user)
    tokenized_input = [word.lower() for word in tokenized_input]
    add,sub = words_of_comparison(prev_input,tokenized_input)

    n = len(add)

    if len(prev_input)>=1 and prev_input[-1] in NEGATION_LIST:
        add[0] = "negexdel"
    
    for i in range(n):
        if add[i] in NEGATION_LIST:
            add[i] = "negex"
            if i!=n-1:
                add[i+1]="negexdel"
        if add[i] not in data:
            add[i] = SpellCheckerWithUnknown(add[i],ABBREVIATIONS,MEDICAL_TERMS)
    for i in range(len(sub)):
        if sub[i] not in data:
             sub[i] = SpellCheckerWithUnknown(sub[i],ABBREVIATIONS,MEDICAL_TERMS)

    for word in add:
        if word in data:
            x = data[word]
            addScore(algorithm_scoring,algorithm_node_scoring,x)
    for word in sub:
        if word in data:
            x = data[word]
            subScore(algorithm_scoring,algorithm_node_scoring,x)
    
    return tokenized_input
    

            
    

