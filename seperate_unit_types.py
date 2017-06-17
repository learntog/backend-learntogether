import json
classes = json.load(open("classes.json"))

upload = {}

def GetTextOnly(s):
    return ''.join([i for i in s if not i.isdigit()])


for cl in classes:
    cll = cl.split("*")
    #check if the unit is present
    unit = cll[0]
    if(unit not in upload):
        upload[unit] = {}
    type = GetTextOnly(cll[1])
    if(type not in upload[unit]):
        upload[unit][type] = []
    upload[unit][type].append(cl)

from firebase import firebase
firebase = firebase.FirebaseApplication('https://learntogether-a250b.firebaseio.com/')

firebase.put('','seperate_unit_list/', upload)






