#importeer de nodige onderdlen uit de extensies (door niet heel de extensie te laden werkt de codering sneller)
from snap7 import client
from json import dump, loads
from os import getcwd, listdir

#defineer de logfile de orders map 
path_orders = getcwd() + "\Json\orders"
path_log = getcwd() + "\Json\Log\log.json"

#plc database informatie
DBnumber = 100      #start adres
Start = 0           #start binnen adres
Size = 12           #aantial bits

#PLC definieren en connecteren
PLC = client.Client()
PLC.connect('192.168.0.1', 0, 0)

#Funcitie die plc uitleest voor nieuwe order
def Read_PLC():
    TrakcingID_New = ListOfUnwriten()
    END = bool.from_bytes(db[10:12], byteorder='big')
    if END == True and (len(TrakcingID_New) != 0):
        Write_PLC(TrakcingID_New)
    
def Update_Active_ID(TrakcingID_New):
    with open(path_log) as f:
        data = {
               "Active_ID": TrakcingID_New[0] 
            }
        dump(data, open(path_log, "w"), ensure_ascii=False, indent=4)
    f.close()

#Funcite die de plc nieuwe order opstuurt 
def Write_PLC(TrakcingID_New):
    a = 1
    x = int(directory(str(path_orders), ".json"))
    while a <= x:
        file = open(path_orders + f"\order{a}.json", "r")
        data = loads(file.read())
        if TrakcingID_New[0] == data["TrackingID"]:
            R = int(data["R"])
            G = int(data["G"])
            B = int(data["B"])
            G_K = int(data["Big_Small"])
            Location = int(data["Location"])
            END = bool(False)
            db[0:2] = R.to_bytes(2, 'big')
            db[2:4] = G.to_bytes(2, 'big')
            db[4:6] = B.to_bytes(2, 'big')
            db[6:8] = G_K.to_bytes(2, 'big')
            db[8:10] = Location.to_bytes(2, 'big')
            db[10:12] = END.to_bytes(2, 'big')
            PLC.db_write(DBnumber, Start, db)
            Update_Active_ID(TrakcingID_New)
            print(f"order{a} geupload naar plc")
            file.close()
            break
        else:
            file.close()
            a += 1
    pass

#Fucnctie om te dedecteren welke orders niet zijn gestart
def ListOfUnwriten():
    ID_list = []
    a = 1
    x = int(directory(str(path_orders), ".json"))
    while a <= x:
        file = open(path_orders + f"\order{a}.json", "r")
        data = loads(file.read())
        if "" == data["CardID"]:
            ID_list.append(data["TrackingID"])
            a += 1
        else:
            a += 1
    
    return ID_list

#Fucntie voor aantal files in de map orders te vinden
def directory(path_a, extension):
    list_dir = listdir(path_a)
    count = 0
    for file in list_dir:
        if file.endswith(extension):
            count += 1
    return count

#Als status van de plc actief is ...
state = PLC.get_cpu_state()
if state == "S7CpuStatusRun":
    print('PLC: Running')  
#als file actief blijf plc uitlezen
while True:
    db = PLC.db_read(DBnumber, Start, Size)
    Read_PLC()

