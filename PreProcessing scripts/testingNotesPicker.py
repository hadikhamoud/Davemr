import os
import random
from random import randrange
from bs4 import BeautifulSoup


filesDir = '/Users/hadihamoud/Downloads/www/emr/DiagnosesXML/Annotated'



files = os.listdir(filesDir)
chosen = []

start = '<notes>\n'
end = '</notes>'



filew = open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/Dave-server/data/XML files/notesfortestingAnnHadi.xml','w')

filew.write(start)

for i in range(0,10):
    choice = randrange(len(files))
    chosen_file = files[choice]
    with open(os.path.join(filesDir,chosen_file),'r') as f:
                data = f.read()
    Bs_data = BeautifulSoup(data,'xml')  
    b_notes = Bs_data.find_all('note')
    for j in range(0,3):
        choice_note = randrange(len(b_notes))
        chosen_note = b_notes[choice_note]
        filew.write(str(chosen_note))
filew.write(end)
filew.close()

    