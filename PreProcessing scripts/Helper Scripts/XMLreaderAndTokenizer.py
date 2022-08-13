from bs4 import BeautifulSoup
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
from negspacy.termsets import termset
from spellchecker import SpellChecker


ts = termset("en_clinical")
ts.add_patterns({
        'preceding_negations':['-',' -']
        })
neg_termset=ts.get_patterns()
negation_list=neg_termset['preceding_negations']

nltk.download('averaged_perceptron_tagger')
nltk.download('words')

correct_words = words.words()
lemmatizer = WordNetLemmatizer()


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

MedicalFileR = open(os.path.join(CURRENT_DIR,'data/testdatahashmaps/MedicalTermsDict.txt'),'r')
AbbreviationsFileR = open(os.path.join(CURRENT_DIR,'data/testdatahashmaps/AbbreviationsOnly.txt'),'r')
MedD = json.load(MedicalFileR)
AbbrD = json.load(AbbreviationsFileR)

# original = []
# lemma = []
# tag = []
# df = pd.DataFrame({'Original':original,"tag": tag, "lemma":lemma})
# JSON_dict = '/Users/hadihamoud/Desktop/FYPEPIC/FYP/data/jsontest.txt'
# f = open(JSON_dict,'r')
# BigData = json.load(f)


#autocorrection using english corpus before lemmatization
#limit high frequency (i.e: '.')
#nltk neg ex(negation extraction) since no might be high frequency(no,without...)

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


def lemmetize_print(words,AbbrD,MedD):
     originalNeg = word_tokenize(words)
     original = []
     originalNegEx = SpellCheckerWithUnknown(originalNeg,AbbrD,MedD)
     lemma = []
     tag = []

     i = 0
     length= (len(originalNegEx))


     while i<length-1:
         if originalNegEx[i] not in negation_list:
             original.append(originalNegEx[i])
         else:
             i+=1
         i+=1

     for token in original:
          lemmetized_word = lemmatizer.lemmatize(token)
          lemma.append(lemmetized_word)
    
          
     
     tags = nltk.pos_tag(original)
     for t in tags:
         tag.append(t[1])

          
    
     Results = [original,tag,lemma]
     return Results


def Writetofile(filew,dir):
    st_tag = '<p>'
    end_tag = '</p>'
    fw = open(filew,'w')
    i = 0
    
    for filer in os.listdir(dir):
        try:
            print(i,': ',filer)
            with open(os.path.join(dir,filer),'r') as f:
                data = f.read()
            Bs_data = BeautifulSoup(data,'xml')
            
            b_text = Bs_data.find_all('text',text = True)
            for text in b_text:
                fw.write(st_tag+'\n')
                # df = lemmetize_print(text.text)
                # df = df.loc[1:,:]
                results = lemmetize_print(text.text,AbbrD,MedD)
                for index in range(len(results[0])):
                    fw.write(results[0][index]+'\t'+results[1][index]+'\t'+results[2][index]+'\n')
                fw.write(end_tag+'\n')
            i+=1
        except:
            continue
            
            

        
    fw.close()
    return 'Success!'



Writetofile('unannotated_LowerCase_AutoCorrect_NEGEX.LEMMATIZED','/Users/hadihamoud/Downloads/www/emr/DiagnosesXML/Unannotated')

# loop for finding correct spellings
# based on jaccard distance
# and printing the correct word





































    #  pprint({a[i] : tokens[i] for i in range(len(a))}, indent = 1, depth=5)
     


# print(lemmetize_print(b_text[1].text).head())
# def pos_tagger(nltk_tag):
#     if nltk_tag.startswith('J'):
#         return wordnet.ADJ
#     elif nltk_tag.startswith('V'):
#         return wordnet.VERB
#     elif nltk_tag.startswith('N'):
#         return wordnet.NOUN
#     elif nltk_tag.startswith('R'):
#         return wordnet.ADV
#     else:         
#         return None






# b_name = Bs_data.find('note', {'firstName':44226})







# i = 0
# while i <20:

#     with open('/Users/hadihammoud/Desktop/FYPEPIC/DISCO/testemrcorpus'+str(i)+'.tok','w') as fw:
#         fw.write('<doc>\n')

#         for x in b_text:
#             x = str(x)
#             x = x.replace('<text>','<p>\n')
#             x = x.replace('</text>','\n</p>\n')
#             fw.write(x)


