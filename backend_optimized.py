import datetime
import json
import os.path

import pyrebase
"""
TODO:
"""
#TODO add file check (is legit text file)
#TODO only add semester 1


from firebase import firebase
firebase = firebase.FirebaseApplication('https://learntogether-a250b.firebaseio.com/')

config = {
    'apiKey': "AIzaSyBLA6sDqXwnMX6tJayM4dmYCPRzt5CW91M",
    'authDomain': "learntogether-a250b.firebaseapp.com",
    'databaseURL': "https://learntogether-a250b.firebaseio.com",
    'storageBucket': "learntogether-a250b.appspot.com",
}


pybase = pyrebase.initialize_app(config)


allclasses = None
if os.path.exists("classes.json"):
    j = open("classes.json", 'r+')
    allclasses = json.load(j)
    j.close()
else:
    allclasses = firebase.get("","classes/")
    j = open("classes.json", 'w')
    json.dump(allclasses, j)
    j.close()

print(allclasses)



storage = pybase.storage()

def fileReader(firebase, file, user):
    unitFile = open(file, 'r')
    unitList = []

    for line in unitFile:
        unitList.append(line)

    unitFile.close()
    unitStored = []

    for i in range(1,len(unitList)):
        unitLine = unitList[i].strip().split("\t")
        unitName = unitLine[0].split("_")
        unitLine[0]=unitName[0]
        unitStrip = []
        unitStrip.append(unitLine[0])
        unitStrip.append(unitLine[2]+unitLine[3])
        unitStrip.append(unitLine[4]+unitLine[5])
        unitStrip.append(unitLine[7].replace("/","-"))
        unitStrip.append(unitLine[2])
        unitStrip.append(unitLine[3])
        if unitLine[9][1] == ".":
            unitLine[9] = unitLine[9][:3]
        else:
            unitLine[9] = unitLine[9][0]
        unitStrip.append(unitLine[9])
        unitStored.append(unitStrip)


    unitOut = unitStored

    unitSimple = []
    unitSimpleTemp = []
    for unitRef in unitOut:
        unitStore = unitRef[0]+"*"+unitRef[1]+"*"+unitRef[2][0:3]+"*"+unitRef[2][3:]+"*"+unitRef[3]+"*"+unitRef[-1].replace(".", "~")
        unitStoreTemp = unitRef[0]+"*"+unitRef[1]+"*"+unitRef[2][0:3]+"*"+unitRef[2][3:]+"*"+unitRef[3]+"*"+unitRef[-1].replace(".", "~")

        # print(unitStore, unitStoreTemp)

        unitSimple.append(unitStore)
        unitSimpleTemp.append(unitStoreTemp)
    unit = unitSimple
    #print(unit)
    #print()
    unitTemp = unitSimpleTemp


    firebase.put("", "users/" + str(user[0]) + "/classes", unitTemp)

    newUnit = []
    for p in range(len(unit)):
        newUnit.append([])

    for x in range(len(unit)):
        newUnit[x].append(unitOut[x][0])
        newUnit[x].append(unitOut[x][4])
        newUnit[x].append(unitOut[x][5]+unitOut[x][2])

    #print(unit, newUnit)

    oldUsers = []
    for n in range(len(unit)):
        oldUsers.append([])
    temp = []

    for x in range(len(unit)):
        try:
            #a = firebase.get('','classes/'+unit[x]+'/users/')
            #print(unit[x])

            a = allclasses[unit[x]]['users']

            temp.append(a)

            if temp[x] not in oldUsers[x] and temp[x] is not None:
                oldUsers[x].extend(temp[x])

            if user[0] not in oldUsers[x]:
                oldUsers[x].extend(user)
        except Exception as e:
            firebase.put('/', 'requests/' + str(user[0]) + "/status", 'ERR'+str(e))

    for i in range(len(unit)):
        dictionary = {'users':oldUsers[i]}
        firebase.put("","classes/"+str(unit[i]),dictionary)
        allclasses[str(unit[i])] = dictionary

    j = open("classes.json", 'w')
    json.dump(allclasses, j)
    j.close()


    firebase.put('/', 'requests/' + str(user[0]) + "/status", 'SUCCESS')
    #End of function


### Main


requests = firebase.get('/','requests/')
#print(requests)
#Download all the files

for request in requests:
    if(requests[request]['status'] == "UPLOAD"):
        storage.child("usertimetable/"+request).download("user_files/"+request)
        firebase.put('/','requests/'+request+"/status", 'DOWNLOADED')



for request in requests:
    if(requests[request]['status']!="SUCCESS"):
        user = request
        fileReader(firebase, "user_files/"+user, [user])



#
# file = 'timetable-10001000.txt'
# user = ["Ishan"]
# fileReader(firebase, file, user)






#storage.child("hey/28809033.txt").download("288090331.txt")
