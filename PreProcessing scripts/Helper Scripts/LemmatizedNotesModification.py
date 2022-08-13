import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

filer = os.path.join(CURRENT_DIR,'/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/Lemmatized Files/annotated_LowerCase_AutoCorrect_NEGEX.LEMMATIZED')


def ModifyLine(L):
    n = len(L)
    if n>1:
        L[0] = L[0].lower()
        L[2] = L[2].lower()
    
        
for i in range(20):
    f = open(filer,'r')
    filew = open(filer[:-11]+"ModifiedLowerC"+str(i)+".LEMMATIZED","w")
    content = f.readlines()
    for line in content:
        tempLine = line.split("\t")
        ModifyLine(tempLine)
        strLine = '\t'.join([str(item) for item in tempLine])
        filew.write(strLine)

    filew.close()




