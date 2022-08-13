import csv              
f = open(r'/Users/hadihammoud/OneDrive - American University of Beirut/annotatednotes.csv')
csv_f = csv.reader(f)   
data=[]
for row in csv_f: 
	data.append(row)
f.close()


def convert_row(row):
   return """<note>
   <recordID>%s</recordID>
   <caseCode>%s</caseCode>
   <docCode>%s</docCode>
   <firstName>%s</firstName>
   <lastName>%s</lastName>
   <Anon>%s</Anon>
   <date>%s</date>
   <ageGrp>%s</ageGrp>
   <sex>%s</sex>
   <nbOfDx>%s</nbOfDx>
   <DxList>%s</DxList>
   <DxDesc>%s</DxDesc>


   



</note>""" % (
   row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],row[9],row[10],row[11])

with open('annotatednotes.xml', 'w') as f: f.write('\n'.join([convert_row(row) for row in data[1:]]))


# row.['Record ID'], row.['Case ID'], row.['Case ID'], row.['First Name'], row.['Last Name'], row.['Note Text'], row.['Age Group'], row.['Sex'], row.['Number of Diagnoses'],row.['Diagnosis Code'],row.['Diagnosis Description'])