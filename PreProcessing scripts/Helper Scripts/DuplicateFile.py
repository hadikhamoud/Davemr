import os

filer = open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/Lemmatized Files/annotated_LowerCase_AutoCorrect_NEGEX.LEMMATIZED','r')
content = filer.read()

for i in range(20):
    filew = open('/Users/hadihamoud/Desktop/FYPEPIC/DISCO/DISCOBuilder-1.1.1/allnotesAutoCorrectedNegex-lemmatized/'+'annotated_LowerCase_AutoCorrect_NEGEX'+str(i)+'.LEMMATIZED','w')
    filew.write(content)
    filew.close()

