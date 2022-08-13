import json

with open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/data/jsontest.txt','r') as file:
    data = json.load(file)
    print(len(data))
    for key, value in data.items():
        print(key,' : ',value)



# with open('/Users/hadihamoud/Desktop/FYPEPIC/FYP/data/jsontestemr.txt','r') as file:
#     datak = json.load(file)
#     print(len(datak))



