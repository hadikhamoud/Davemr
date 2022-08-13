from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import os
import json
from negspacy.termsets import termset
from spellchecker import SpellChecker

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MedicalFileR = open(os.path.join(CURRENT_DIR,'testdatahashmaps/MedicalTermsDict.txt'),'r')
AbbreviationsFileR = open(os.path.join(CURRENT_DIR,'testdatahashmaps/AbbreviationsOnly.txt'),'r')
MedD = json.load(MedicalFileR)
AbbrD = json.load(AbbreviationsFileR)

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


lemmatizer = WordNetLemmatizer()

ts = termset("en_clinical")
ts.add_patterns({
        'preceding_negations':['-',' -']
        })
neg_termset=ts.get_patterns()
negation_list=neg_termset['preceding_negations']

nltk.download('averaged_perceptron_tagger')
nltk.download('words')



def lemmetize_print(words):

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


#turn annotations into a dictionary to add them to the notes one by one
def annotationsToDict(annotations):
    labelAndAnnotation={}
    b_annotation = annotations[0].find_all('annotation')
    if len(b_annotation)!=0:
        for annotation in b_annotation:
            b_label = annotation.find('label',text=True)
            b_annotatedText = annotation.find('annotatedText',text=True)
            tokenizedText = word_tokenize(b_annotatedText.text)
            for token in tokenizedText:
                labelAndAnnotation[token]=b_label.text
    return labelAndAnnotation


    

def WritetofileAnnotated(filew,dir):
    st_tag = '<p>'
    end_tag = '</p>'
    fw = open(filew,'w')
    filer=dir
  
    with open(os.path.join(dir,filer),'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data,'xml')

    b_note = Bs_data.find_all('note')
    #for each note
    for note in b_note:
        b_text = note.find_all('text',text=True)
        b_annotations = note.find_all('annotations')
        #search for text and turn annotations into dictionary with
        #keys as the word and values being the label
        if b_annotations:
            labelAndAnnotation = annotationsToDict(b_annotations)
        else:
            labelAndAnnotation={}
        for text in b_text:
            fw.write(st_tag+'\n')
            results = lemmetize_print(text.text)
            for index in range(len(results[0])):
                token = results[0][index]
                #if the word is annotated (i.e in the dictionary)
                if labelAndAnnotation and token in labelAndAnnotation:
                    label = labelAndAnnotation[token]
                    #write the label then DAVETAG then the label again
                    fw.write(label+'\t'+'DAVETAG'+'\t'+label+'\n')
                    fw.write(token+'\t'+results[1][index]+'\t'+results[2][index]+'\n')
                    #fw.write(label+'\t'+'DAVETAG'+'\t'+label+'\n')
                else:
                    #if not found, write it on its own
                    fw.write(token+'\t'+results[1][index]+'\t'+results[2][index]+'\n')

            fw.write(end_tag+'\n')
        

        
    fw.close()
    return 'Success!'



WritetofileAnnotated('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/Lemmatized Files/annotated_LowerCase_AutoCorrect_NEGEX.LEMMATIZED','/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/XML files/AllAnnotated.xml')

