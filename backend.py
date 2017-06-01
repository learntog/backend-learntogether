from firebase import firebase
firebase = firebase.FirebaseApplication('https://learntogether-a250b.firebaseio.com/')

def fileUpload(firebase,file,user):
    unitFile = open(file, 'r')
    unitList = []

    #converts file into readable format (i.e. List)
    for line in unitFile:
        unitList.append(line)

    unitFile.close()
    unitStored = []
    #converts into usable name
    # 0 - Unit Code
    # 2 - Group
    # 3 - Session
    # 4 - Day && 5 - Time
    # 7 - Location
    #uniStored[4] = group
    #uniStored[5] = activity

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

    print("unitStored",unitStored)

    unit = []
    for item in unitStored:
        unitStore = item[0] + "*" + item[1] + "*" + item[2] + "*" + item[3] + "*" + item[6]
        unit.append(unitStore)

    print("unit", unit)

    newUnit = [] #all units from single user
    for p in range(len(unit)):
        newUnit.append([])

    for x in range(len(unit)):
        newUnit[x].append(unitStored[x][0])
        newUnit[x].append(unitStored[x][4])
        newUnit[x].append(unitStored[x][5]+unitStored[x][2])

    firebase.put("","users/"+user+"/classes", unit)

    classes = firebase.get("","/classes/")
    print("classes", classes)

    # if classes != None:
    #     for each in unit:
    #         if each in classes:
    #             tempUsers = []
    #             for x in range(len(unit)):
    #                 tempUsers.append(firebase.get('', '/classes/' + unit[x] + '/users/'))
    #                 if user not in tempUsers[x]:
    #                     tempUsers[x].append(user)
    #
    #             print("Temp:   ", tempUsers)
    #
    #             dictionary = ""
    #             for i in range(len(unit)):
    #                 dictionary = {'location': unitStored[i][3], 'time': unitStored[i][2], 'unitID': unitStored[i][0],
    #                               'group': unitStored[i][1], 'users': tempUsers[i]}
    #                 firebase.put("", "/classes/" + str(unit[i]), dictionary)
    # else:
    
    dictionary = ""
    for i in range(len(unit)):
        dictionary = {'location': unitStored[i][3], 'time': unitStored[i][2], 'unitID': unitStored[i][0],'group': unitStored[i][1], 'users': [user]}
        firebase.put("", "/classes/" + str(unit[i]), dictionary)

file = 'timetable-10001000.txt'
user = "test5"

fileUpload(firebase,file,user)
