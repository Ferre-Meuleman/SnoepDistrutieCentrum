#importeer de nodige extensies
from json import dump, loads, load
from os import getcwd, listdir
from serial import Serial
from snap7 import client

# definieer de seriele poort en snelheid
ser = Serial('com5', 9600)
ser.flushInput()

# definieer de JSON map
path_orders = getcwd() + "\Json\orders"
path_log = getcwd() + "\Json\Log\log.json"

# PLC data waardes
DBnumber = 100
Start = 0
Size = 12

# PLC connectie opstarten
PLC = client.Client()
PLC.connect('192.168.0.1', 0, 0)

print("Arduino klaar")

# lees de seriele monitor
def ReadSerial(): 
    ser_bytes = ser.readline()[:-2]
    ser_bytes2 = ser_bytes.decode("utf-8")
    
    
    decoded_bytes = ser_bytes2
    if ("Reader 0: " in decoded_bytes):
        step1 = decoded_bytes.replace(f"Reader 0:  ", "")
        CardID = step1.replace(",","")
        TrackingID = Active_TrackingID()
        serial_TrackingID = str(TrackingID + "#")
        ser.write(serial_TrackingID.encode())
        Location = 1
        Update_Location_CardID(CardID, Location, TrackingID)
    
    elif (decoded_bytes == "MIFARE_Write() success: "):
        pass
    
    elif (decoded_bytes == "PCD_Authenticate() failed: " or decoded_bytes == "MIFARE_Write() failed: "):
        print("failed")

    elif ("Reader " in decoded_bytes and "Reader 0" not in decoded_bytes):
        step2 = bytes
        i = int(decoded_bytes[7])
        step1 = decoded_bytes.replace(f"Reader {i}:  ", "")
        step2 = step1.split(", ")
        CardID = step2[0]
        TrackingID = step2[1]
        # print(CardID, TrackingID)  
        Location = i + 1
        Update_Location(CardID, Location, TrackingID)

# functie om de de locatie te updaten in json
def Update_Location(CardID, Location, TrackingID):
    a = 1
    x = int(directory(str(path_orders), ".json"))
    while a <= x:
        file = open(path_orders + f"\order{a}.json", "r")
        data =  loads(file.read())
        if CardID == data["CardID"] and TrackingID == data["TrackingID"]:
            data = {
                "orderID": data["orderID"],
                "FirstName": data["FirstName"],
                "LastName": data["LastName"],
                "R": data["R"],
                "G": data["G"],
                "B": data["B"],
                "Big_Small": data["Big_Small"],
                "Location": Location,
                "CardID": data["CardID"],
                "TrackingID": data["TrackingID"]
            }

            with open(path_orders + f"\order{a}.json", 'w', encoding='utf-8') as f:
                dump(data, f, ensure_ascii=False, indent=4)
                f.close()
            print(f"order{a} locatie geupdate naar: {Location}")
            Location = int(Location)
            db[8:10] = Location.to_bytes(2, 'big')
            PLC.db_write(DBnumber, Start, db)
            break
        else:
            a = a + 1

# funcie om de Card ID en locatie te updaten 
def Update_Location_CardID(CardID, Location, TrackingID):
    a = 1
    x = int(directory(str(path_orders), ".json"))
    while a <= x:
        file = open(path_orders + f"\order{a}.json", "r")
        data =  loads(file.read())
        if data["CardID"] == "" and TrackingID == data["TrackingID"]:
            data = {
                "orderID": data["orderID"],
                "FirstName": data["FirstName"],
                "LastName": data["LastName"],
                "R": data["R"],
                "G": data["G"],
                "B": data["B"],
                "Big_Small": data["Big_Small"],
                "Location": Location,
                "CardID": CardID,
                "TrackingID": data["TrackingID"]
            }
            file.close()
            with open(path_orders + f"\order{a}.json", 'w', encoding='utf-8') as f:
                dump(data, f, ensure_ascii=False, indent=4)
                f.close()
                      
            db[8:10] = int(Location).to_bytes(2, 'big')
            PLC.db_write(DBnumber, Start, db)
            print(f"order{a} locatie geupdate naar: {Location}")
            break
        else:
            a += 1

# Lees de actieve id
def Active_TrackingID():
    with open(path_log) as f:
        data = load(f)
        Active_TrackingID = data["Active_ID"]
    f.close()
    return Active_TrackingID

# lees de eerste ongeschreven bestelling
def ListOfUnwriten():
    ID_list = []
    a = 1
    x = int(directory(str(path_orders), ".json"))
    while a <= x:
        file = open(path_orders + f"\order{a}.json", "r")
        data =  loads(file.read())
        if "" == data["CardID"]:
            ID_list.append(data["TrackingID"])
            a += 1
        else:
            a += 1
    return ID_list

# aantal files in een bepaalde map
def directory(path_a, extension):
    list_dir = listdir(path_a)
    count = 0
    for file in list_dir:
        if file.endswith(extension):
            count += 1
    return count

# terwijl actief
while True:
    db = PLC.db_read(DBnumber, Start, Size)
    ReadSerial()
