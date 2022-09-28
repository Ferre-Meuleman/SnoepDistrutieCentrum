# importeer de nodige onderdlen uit de extensies (door niet heel de extensie te laden werkt de codering sneller)
from subprocess import run
from os import getcwd
from time import sleep
from threading import Thread

# Path naar alle files
Arduino = getcwd() + "\\Python\\Arduino.py"
PLC = getcwd() + "\\Python\\PLC.py"
Website = getcwd() + "\\Website\\app.js"

# Alle files klaarzetten per Thread
t1 = Thread(target=run, args=(["python", Arduino],))
t2 = Thread(target=run, args=(["python", PLC],))

# Start elke Thread
t1.start()
sleep(1)
t2.start()

# Zorg dat elke Thread actief blijft
t1.join()
sleep(1)
t2.join()
