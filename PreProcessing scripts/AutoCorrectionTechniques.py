import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from pprint import pprint
from nltk.corpus import wordnet
import pandas as pd
import os
import json
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
from nltk.corpus import words
from textblob import TextBlob
from spellchecker import SpellChecker
import jamspell



#testXML = open("","r")
# data = testXML.read()
# Bs_data = BeautifulSoup(data,'xml')

# teststr=""

# b_text = Bs_data.find_all('text',text = True)

# for text in b_text:
#     teststr = text.text


teststr1 = 'still c/o R knee pain, episodes of giving way and foreign body sensation\nreports as well stiffness, hearing cracking inside R knee\nPE: pain all over, despite normal ROM\nI/P: medial meniscal lesion v/s "simulation"\nProxen 500 bid + Peptazol\nDo MRI of KNee\nUcx contaminated >>>repeat\nU/S pelvis showed lesion over R vary to be reevaluated in 10 weeks >>>Request given'

teststrCorr="""rt knee pain of 5 days  duration .was seen 5 days ago , given proxen 500 bid.

presented for folloe up  on knee pain.
pt was fine all the week end , but has pain today again , while rising from the squatting position . he also felt a click and since then the crepitation returned.
no swelling ano edam ,, no hotness.
grinding sign positive.
medial anterrioir joint direct pain.
assememt .medial meniscal tear?
plan continue Proxen bid and follow up in 1 week
"""
teststr="""rt knee pain of 5 days  duration .was seen 5 days ago , given proxen 500 bid.

presented for follow up  on knee pain.
pt was fine all the week end , but has pain today again , while rising from the squatting position . he also felt a click and since then the crepitation returned.
no swelling ano edam ,, no hotness.
grinding sign positive.
medial anterior joint direct pain.
assessment .medial meniscal tear?
plan continue Proxen bid and follow up in 1 week
"""

test = """78 yrs old patient for right knee pain &gt; left. She has a fall 8 yrs ago, since then she has fracture of rotula treated orthopedically.  
Has done stent twice (has 3 stents). Takes 8 medications for heart. Corvasal, Concor 5 1/d, Liponorm 10 mg 1/d, Nefazan 75, Rabec 10 mg, Aspirin protect.

Exam : BP = 16/8 rt, 14/8 left, pulse regular, Systolic bruit raditaing to the neck max on aortic foyer. No leg edema, Pulm auscult nl. Pain in both knees on fexion, and crackles on knee flexion, flexion limited in right knee by pain.

Impression: Osteoarthritis of knees? Do x-ray and Give Panadol SOS and Fastum gel. Preview vaccination (Pneumo 23 and flu), Ca + vit D , BMD testing?"""


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


MedicalFileR = open(os.path.join(CURRENT_DIR,'testdatahashmaps/MedicalTermsDict.txt'),'r')
AbbreviationsFileR = open(os.path.join(CURRENT_DIR,'testdatahashmaps/AbbreviationsOnly.txt'),'r')
MedD = json.load(MedicalFileR)
AbbrD = json.load(AbbreviationsFileR)



original = word_tokenize(teststrCorr)
Corrected = word_tokenize(teststrCorr)

correct_words = words.words()
lemmatizer = WordNetLemmatizer()

def AutoCorrectJaccard(words,correct_words = correct_words):
    output = []
    for word in words:
        try:
            temp = [(jaccard_distance(set(ngrams(word, 2)),
            set(ngrams(w, 2))),w) for w in correct_words if w[0]==word[0]]
            output.append(sorted(temp, key = lambda val:val[0])[0][1])
        except:
            output.append(word)
    return output

def JaccardTop3Closest(word,correct_words = correct_words):
    temp = [(jaccard_distance(set(ngrams(word, 2)),
    set(ngrams(w, 2))),w) for w in correct_words if w[0]==word[0]]
    return sorted(temp, key = lambda val:val[0])[0:3]


def JaccardSpellCheckerHybrid(words,thresh=0.2,correct_words = correct_words):
    output = []
    spell = SpellChecker()
    for word in words:
        try:
            temp = [(jaccard_distance(set(ngrams(word, 2)),
            set(ngrams(w, 2))),w) for w in correct_words if w[0]==word[0]]
            Topword = sorted(temp, key = lambda val:val[0])[0]
            if Topword[0]<=thresh:
                output.append(Topword[1])
            elif Topword[0]>thresh and Topword<0.05:
                output.append(spell.correction(word))
            else:
                output.append(word)
        except:
            output.append(word)
    return output


def JaccardSpellCheckerHybridWord(word,thresh=0.2,correct_words = correct_words):

    try:
        spell = SpellChecker()
        temp = [(jaccard_distance(set(ngrams(word, 2)),
        set(ngrams(w, 2))),w) for w in correct_words if w[0]==word[0]]
        Topword = sorted(temp, key = lambda val:val[0])[0]
        if Topword[0]<=thresh:
            return Topword[1]
        elif Topword[0]>thresh and Topword<0.05:
            return spell.correction(word)
        else:
            return word
    except:
        return word


def SpellCheckerWithUnknown(words,AbbrD,MedD):
    output = []
    spell = SpellChecker()
    for word in words:
        misspelled = spell.unknown([word.lower()])
        if len(misspelled)!=0:
            misspelled_word = misspelled.pop()
            if misspelled_word not in AbbrD and misspelled_word not in MedD:
                output.append(spell.correction(word))
            else:
                output.append(word)
        else:
            output.append(word)
    return output








def TextBlobCorrectWord(word):
    correct = TextBlob(word)
    return str(correct.correct())

def TextBlobCorrect(words):
    output = []
    for word in words:
        correct_word = TextBlob(word)
        output.append(str(correct_word.correct()))
    return output


def PySpellChecker(words):
    output = []
    spell = SpellChecker()
    for word in words:
        output.append(spell.correction(word))
    return output

def PySpellCheckerWord(word):
    spell = SpellChecker()
    return spell.correction(word)


def JamSpellCorrect(words):
    output=[]
    spell = jamspell.TSpellCorrector()
    spell.LoadLangModel('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/en.bin')
    for word in words:
        output.append(spell.FixFragment(word))
    return output

def JamSpellCorrectWord(word):
    spell = jamspell.TSpellCorrector()
    spell.LoadLangModel('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/en.bin')
    return spell.FixFragment(word)


#Hidden markov model
#window
#distributional similarity maa l window kello
#adde proxen maa 1 w adde proxen maa 2
#try to correct the word
#threshold for notes w for pubmed
#check the top three diseases
#discritization
#graphing all disco words


def SimilarityMeasure(Original,SpellChecked):
    n = len(Original)
    diff = 0
    differences = {}
    for ori,spel in zip(Original,SpellChecked):
        if ori!=spel:
            diff+=1
            differences[ori]=spel
    Accuracy = (n-diff)/n
    return differences, diff, round(Accuracy,4)*100


mode = input("choose mode 1 or 2: ")

if int(mode)==1:
    n=' '
    while n!="END":
        n=input("enter word: ")
        print("Jaccard:",JaccardTop3Closest(n))
        print("TextBlob:",TextBlobCorrectWord(n))
        print("PySpellChecker:",PySpellCheckerWord(n))
        print("JamSpell: ",JamSpellCorrectWord(n))
        print("Jaccard And PySpellChecker Hybrid: ",JaccardSpellCheckerHybridWord(n))
else:
        print("------------original----------\n")
        # print(original)

        print("------------Jaccard----------\n")

        ACJ = AutoCorrectJaccard(original)
        print(SimilarityMeasure(Corrected,ACJ))

        print("------------TextBlob----------\n")

        TBC = TextBlobCorrect(original)
        print(SimilarityMeasure(Corrected,TBC))


        print("------------PySpellChecker----------\n")

        PSC = PySpellChecker(original)
        print(SimilarityMeasure(Corrected,PSC))


        print("------------JamSpell----------\n")

        JSC = JamSpellCorrect(original)
        print(SimilarityMeasure(Corrected,JSC))


        print("------------Jaccard and SpellChecker Hybrid----------\n")

        JSCH = JaccardSpellCheckerHybrid(original,thresh=0)
        print(SimilarityMeasure(Corrected,JSCH))


        print("------------Spell Checker with Unknown----------\n")

        SCU = SpellCheckerWithUnknown(original,AbbrD,MedD)
        print(SimilarityMeasure(Corrected,SCU))
