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

pwd = "ishan4899qwert123"
import pyrebase

config = {
    'apiKey': "AIzaSyBLA6sDqXwnMX6tJayM4dmYCPRzt5CW91M",
    'authDomain': "learntogether-a250b.firebaseapp.com",
    'databaseURL': "https://learntogether-a250b.firebaseio.com",
    'storageBucket': "learntogether-a250b.appspot.com",
}

firebase = pyrebase.initialize_app(config)


auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password("ishan@ishanjoshi.me", pwd)
print(user)

# Get a reference to the database service
db = firebase.database()

db.child('seperate_unit_list/').set(upload, user['idToken'])






