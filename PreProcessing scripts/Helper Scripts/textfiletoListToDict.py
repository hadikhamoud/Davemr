
import json
filer = open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/MedicalTermsList.txt')

listOfMedicalTerms = filer.read().split("\n")

DictionaryOfMedicalTerms = {listOfMedicalTerms[i]: 1 for i in range(0, len(listOfMedicalTerms))}


print(DictionaryOfMedicalTerms)


DictionaryOfMedicalTermsJSON = json.dumps(DictionaryOfMedicalTerms) 

filew = open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/MedicalTermsDict.txt','w')

filew.write(DictionaryOfMedicalTermsJSON)

filew.close()


