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

auth = pybase.auth()

# Log the user in


# Get a reference to the database service
db = pybase.database()

if(user!=None):


    allclasses = {}
    if os.path.exists("classes.json"):
        j = open("classes.json", 'r+')
        allclasses = json.load(j)
        if(allclasses == None):
            allclasses = {}
        j.close()
    else:
        allclasses = db.child("classes/").get(user['idToken']).val()
        if (allclasses == None):
            allclasses = {}
        j = open("classes.json", 'w')
        json.dump(allclasses, j)
        j.close()



    storage = pybase.storage()

    def fileReader(firebase, file, curruservalue):
        # print(curruservalue, "Hello excuse me")
        try:
            unitFile = open(file, 'r')
            unitList = []

            for line in unitFile:
                unitList.append(line)

            unitFile.close()
            unitStored = []

            for i in range(1,len(unitList)):
                unitLine = unitList[i].strip().split("\t")
                unitName = unitLine[0].split("_")
                if(unitName[2]!="S1" or unitName[2]=="S1"):
                # if(True):
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
                    unitStrip.append(unitName[2]+"!!2017")
                    unitStored.append(unitStrip)


            unitOut = unitStored

            unitSimple = []
            unitSimpleTemp = []
            for unitRef in unitOut:
                unitStore = unitRef[0]+"*"+unitRef[1]+"*"+unitRef[2][0:3]+"*"+unitRef[2][3:]+"*"+unitRef[3]+"*"+unitRef[-2].replace(".", "~") + "*" + unitRef[-1]
                unitStoreTemp = unitRef[0]+"*"+unitRef[1]+"*"+unitRef[2][0:3]+"*"+unitRef[2][3:]+"*"+unitRef[3]+"*"+unitRef[-2].replace(".", "~") + "*" + unitRef[-1]

                # print(unitStore, unitStoreTemp)

                unitSimple.append(unitStore)
                unitSimpleTemp.append(unitStoreTemp)
            unit = unitSimple

            unitTemp = unitSimpleTemp


            c = {}
            for each in unitTemp:
                c[each] = "S"
            # print(c,"\n", user)
            db.child("/users/").child(curruservalue[0]).child('classes').set(c, user['idToken'])
            # firebase.put("", "users/" + str(user[0]) + "/classes", c)

            newUnit = []
            for p in range(len(unit)):
                newUnit.append([])

            for x in range(len(unit)):
                newUnit[x].append(unitOut[x][0])
                newUnit[x].append(unitOut[x][4])
                newUnit[x].append(unitOut[x][5]+unitOut[x][2])

            print(unit, newUnit)

            oldUsers = []
            for n in range(len(unit)):
                oldUsers.append([])
            print(oldUsers, "\toldusers")
            temp = []


            for x in range(len(unit)):
                try:
                    # a = firebase.get('','classes/'+unit[x]+'/users/')
                    # print(unit[x])



                    if(allclasses.get(unit[x]) is None):
                        print("trueee")
                        allclasses[unit[x]] = {}
                        allclasses[unit[x]]['users'] = []
                        print(allclasses)

                    a = allclasses[unit[x]]['users']

                    print(a, "a")


                    temp.append(a)

                    if temp[x] not in oldUsers[x] and temp[x] is not None:
                        oldUsers[x].extend(temp[x])

                    print(oldUsers, "2")

                    if curruservalue[0] not in oldUsers[x]:
                        oldUsers[x].extend(curruservalue)
                except Exception as e:
                    db.child("/requests/").child(str(curruservalue[0])).child('status').set('ERR' + str(e),
                                                                                            user['idToken'])

            for i in range(len(unit)):
                print(oldUsers, "3")
                sqwer = {}
                for each in oldUsers[i]:
                    sqwer[each] = "A"
                dictionary = {'users': sqwer}
                db.child("classes/").child(str(unit[i])).set(dictionary, user['idToken'])
                allclasses[str(unit[i])] = dictionary
            #     try:
            #         #a = firebase.get('','classes/'+unit[x]+'/users/')
            #         #print(unit[x])
            #
            #
            #         ap = allclasses[unit[x]]['users']
            #         a = []
            #         if(ap is not None):
            #             for each in ap:
            #                 a.append(each)
            #
            #
            #
            #         temp.append(a)
            #
            #         print("a\t", a, "\n", temp, " ", x, "\n", oldUsers)
            #         print()
            #
            #         if temp[x] not in oldUsers[x] and temp[x] is not None:
            #             oldUsers[x].extend(temp[x])
            #
            #         if curruservalue[0] not in oldUsers[x]:
            #             oldUsers[x].extend(curruservalue)
            #
            #
            #     except Exception as e:
            #         pass
            #         # print(e)
            #         #db.child("/requests/").child(str(curruservalue[0])).child('status').set('ERR'+str(e), user['idToken'])
            #         # firebase.put('/', 'requests/' + str(user[0]) + "/status", 'ERR'+str(e))
            #
            # for i in range(len(unit)):
            #     qc = {}
            #     print(oldUsers[i])
            #     for each in oldUsers[i]:
            #         qc[each] = "P"
            #     dictionary = {'users':qc}
            #     print(dictionary)
            #     try:
            #         db.child("classes/").child(str(unit[i])).set(dictionary, user['idToken'])
            #     except Exception as e:
            #         print(e)
            #     # firebase.put("","classes/"+str(unit[i]),dictionary)
            #     allclasses[str(unit[i])] = dictionary

            j = open("classes.json", 'w')
            json.dump(allclasses, j)
            j.close()

            db.child("/requests/").child(str(curruservalue[0])).child('status').set('SUCCESS', user['idToken'])
            # firebase.put('/', 'requests/' + str(user[0]) + "/status", 'SUCCESS')
            #End of function
        except Exception as e:
            print(e)
            db.child("/requests/").child(str(curruservalue[0])).child('status').set('ERR' + str(e), user['idToken'])
            # firebase.put('/', 'requests/' + str(user[0]) + "/status", 'ERROR\t' + str(e))


        ### Main


    requests = db.child("/requests/").get(user['idToken']).val()


    #print(requests)
    #Download all the files

    a = datetime.datetime.now()
    print(a)
    for request in requests:
        if(requests[request]['status'] == "UPLOAD"):
            storage.child("usertimetable/"+request).download("user_files/"+request)
            db.child("/requests/").child(request).child('status').set('DOWNLOADED', user['idToken'])
            # firebase.put('/','requests/'+request+"/status", 'DOWNLOADED')
    b = datetime.datetime.now()
    print(b, b-a)

    for request in requests:
        if(requests[request]['status']!="SUCCESS"):
            userp = request
            fileReader(firebase, "user_files/"+userp, [userp])

    # userp = "TCAEsKIxqvSaI0FQzupsSNmjaIc2"
    # fileReader(firebase, "user_files/" + userp, [userp])
    c = datetime.datetime.now()
    # print(c-b)
else:
    print("Auth failed.")
#
# file = 'timetable-10001000.txt'
# user = ["Ishan"]
# fileReader(firebase, file, user)






#storage.child("hey/28809033.txt").download("288090331.txt")
