#importeer de nodige extensies
from json import loads
from os import getcwd, listdir

path_orders = getcwd() + "\Json\orders"
path_log = getcwd() + "\Json\Log\log.json"

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