from firebase import firebase
firebase = firebase.FirebaseApplication('https://learntogether-a250b.firebaseio.com/')


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
        unitStore = unitRef[0]+"*"+unitRef[1]+"*"+unitRef[2]+"*"+unitRef[3]
        unitStoreTemp = unitRef[0]+"*"+unitRef[1]+"*"+unitRef[2]+"*"+unitRef[3]+ "*" +unitRef[6]
        unitSimple.append(unitStore)
        unitSimpleTemp.append(unitStoreTemp)
    unit = unitSimple
    unitTemp = unitSimpleTemp

    firebase.put("", "users/" + str(user[0]) + "/classes", unitTemp)

    newUnit = []
    for p in range(len(unit)):
        newUnit.append([])

    for x in range(len(unit)):
        newUnit[x].append(unitOut[x][0])
        newUnit[x].append(unitOut[x][4])
        newUnit[x].append(unitOut[x][5]+unitOut[x][2])


    oldUsers = []
    for n in range(len(unit)):
        oldUsers.append([])
    temp = []

    for x in range(len(unit)):
        temp.append(firebase.get('','/classes/'+unit[x]+'/users/'))
        if temp[x] not in oldUsers[x] and temp[x] is not None:
            oldUsers[x].extend(temp[x])

        if user[0] not in oldUsers[x]:
            oldUsers[x].extend(user)

    for i in range(len(unit)):
        dictionary = {'location': unitOut[i][3], 'time': unitOut[i][2], 'unitID': unitOut[i][0], 'group':unitOut[i][1],'users':oldUsers[i]}
        firebase.put("","/classes/"+str(unit[i]),dictionary)

    #End of function


### Main
file = 'timetable-10001000.txt'
user = ["Ishan"]
fileReader(firebase, file, user)
