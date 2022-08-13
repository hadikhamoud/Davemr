import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
from nltk.corpus import words
from spellchecker import SpellChecker
from bs4 import BeautifulSoup

correct_words = words.words()

testXML = open("/Users/hadihamoud/Downloads/www/emr/DiagnosesXML/Unannotated/Inguinal_Hernia.xml","r")
data = testXML.read()
Bs_data = BeautifulSoup(data,'xml')

b_text = Bs_data.find_all('text')
print(len(b_text))


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

def SimilarityMeasure(Original,SpellChecked):
    n = len(Original)
    diff = 0
    differences = {}
    for ori,spel in zip(Original,SpellChecked):
        if ori!=spel:
            diff+=1
            differences[ori]=spel
    Accuracy = (n-diff)/n
    return differences, diff, Accuracy


for text in b_text:
    teststr = text.text
    original = word_tokenize(teststr)
    JSCH = JaccardSpellCheckerHybrid(original,thresh=0)
    print(SimilarityMeasure(original,JSCH))



