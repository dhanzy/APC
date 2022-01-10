import json


f = open('Data.json', 'w')

data = {'District':[
    {'South':'Ekiti South'},
    {'North':'Ekiti North'}
]}

f.write(json.dumps(data, indent=4))
f.close()