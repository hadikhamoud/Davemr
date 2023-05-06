import json
import os
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

MedicalFileR = open(os.path.join(CURRENT_DIR,'data/testdatahashmaps/MedicalTermsDict.txt'),'r')
AbbreviationsFileR = open(os.path.join(CURRENT_DIR,'data/testdatahashmaps/AbbreviationsOnly.txt'),'r')
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

def get_text_score(algos, data, inputofuser, algos1):
    tokenizedinput = nltk.word_tokenize(inputofuser)
    tokenizedinput = [word.lower() for word in tokenizedinput]

    n = len(tokenizedinput)
    for i in range(n-1):
         if tokenizedinput[i]=='NEGEX':
                continue
         if tokenizedinput[i] in negation_list:
                tokenizedinput[i] = 'NEG'
                tokenizedinput[i+1] = 'NEGEX'
                continue
         if tokenizedinput[i] not in data:
             tokenizedinput[i] = SpellCheckerWithUnknown(tokenizedinput[i],AbbrD,MedD)

    for i in range(n-1):
        if tokenizedinput[i] in data:
            x = data[tokenizedinput[i]]
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



#ALGOS SCORING---------------------------------------------------

algos = {}
algos1 ={}
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
algodir = os.path.join(CURRENT_DIR, 'algorithms')

for file in os.listdir(algodir):
    try:
        algos[file] = 0
    except:
        continue
for file in os.listdir(algodir):
    try:
        algos1[file] = []
    except:
        continue


def clearDict():
    global algos
    global algos1
    algos = dict.fromkeys(algos, 0)
    algos1 = dict.fromkeys(algos, [])


#HASHMAP----------------------------------------------------------------------
dictr = 'data/AllOut/jsontestemrNoStopWordsAllNotesAndPubmedv2lowerCaseDiluted12_6.txt'
with open(os.path.join(CURRENT_DIR,dictr),'r') as file:
    data = json.load(file)


#TEST NOTES----------------------------------------------------------------------
filer = 'data/XML files/notesfortestingAnnMira.xml'
test_notes = {}
with open(os.path.join(CURRENT_DIR,filer),'r') as f:
                data_test_notes = f.read()
Bs_data = BeautifulSoup(data_test_notes,'xml')
b_text = Bs_data.find_all('text',text = True)
b_dx = Bs_data.find_all('DxDesc',text = True)

for text,dx in zip(b_text,b_dx):
    test_notes[text.text] = dx.text




#LABELS--------------------------------------------------------------------------
with open(os.path.join(CURRENT_DIR, 'data/excelNameToRealName.txt'), 'r') as file:
    Names = json.load(file)



#SCORING-----------------------------------------------------------------------
i = 0
filew = filer[:-4:]+'Results.txt'
f = open(os.path.join(CURRENT_DIR,filew),'w')
for note in test_notes:
    print('------------------------------- note ',i,'------------------------------------')
    print('Diagnosis Description: ',test_notes[note]+'\n')
    f.write('------------------------------- note '+str(i)+' ------------------------------------\n')
    f.write('Diagnosis Description: '+str(test_notes[note])+'\n')
    print('Our Diagnosis: ')
    get_text_score(algos,data,note,algos1)
    alg = dict(sorted(algos.items(), key=lambda item: item[1]))
    keys = list(alg.keys())
    values = list(alg.values())

    # getTop3Nodes(keys,values,algos1)
    # print([[keys[-1],values[-1]],[keys[-2],values[-2]],[keys[-3],values[-3]]])
    for j in range(1,6):
        f.write(str(Names[keys[-j]])+" : "+str(keys[-j])+' : '+str(values[-j])+'\n')

        print(keys[-j],' : ',values[-j])

    clearDict()
    i+=1
    f.write('\n')
    # NodesSorted = sorted(algos1[keys[-1]],key = lambda item: item[1],reverse = True)
    # print(keys[-1],' : ',NodesSorted[0])
f.close()



