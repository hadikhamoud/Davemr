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


teststr = """2wks hx of rt knee pain mainly when standing  after prolonged sitting ; no swelling ; in 2008 MRI was done -----Mild degeneration of the posterior horns of the medial and lateral menisci. Bone marrow contusion at the level of the tibial plateau and proximal tibial metaphysis. A CT scan of the knee is recommended to rule-out occult fracture. (not done); + recent hx of wt gain

Pex : tenderness at the medial &amp; lateral joint lines ; no crepitations heard

plan ; keep AIrtal bid for 14 ds with PARIET 20 ; try to lose wt"""


teststr2 = """Coming for f/u and to refill her chronic medications
Interval Hx: negative. Her knee pain (L&gt;R) did not change (osteoarthritis). No chest pain/dyspnea. No GI sx. No GI bleed. No urinary sx. No recent change in her appetite/weight.
"""

original = word_tokenize(teststr2)

nltk.download('averaged_perceptron_tagger')
nltk.download('words')

correct_words = words.words()
lemmatizer = WordNetLemmatizer()

def AutoCorrectJaccard(words,correct_words = correct_words):
    output = []
    for word in words:
        try:
            temp = [(jaccard_distance(set(ngrams(word, 2)),
                                        set(ngrams(w, 2))),w)
                        for w in correct_words if w[0]==word[0]]
            output.append(sorted(temp, key = lambda val:val[0])[0][1])
        except:
            output.append(word)
    return output

def JaccardTop3Closest(word,correct_words = correct_words):
    temp = [(jaccard_distance(set(ngrams(word, 2)),
    set(ngrams(w, 2))),w) for w in correct_words if w[0]==word[0]]
    return sorted(temp, key = lambda val:val[0])[0:4]


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


while True:
    n=input("enter word: ")
    print(JaccardTop3Closest(n))
    print(TextBlobCorrectWord(n))
    print(PySpellCheckerWord(n))


# print("------------original----------")
# print(original)

# print("------------Jaccard----------")

# print(AutoCorrectJaccard(original))


# print("------------TextBlob----------")

# print(TextBlobCorrect(original))

# print("------------PySpellChecker----------")

# print(PySpellChecker(original))
