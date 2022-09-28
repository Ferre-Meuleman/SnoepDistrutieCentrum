# Python

This part is made with python due to my previouse experience in python and the posiabliltyes to comunicate with Arduino and PLC.

## Main.py

Usses threading to run file Aruino.py and PLC.py simultaneously.

## Arduino.py

Comunicates between the Arduino and the Json database using serial communication methode. It also communicates a little bit between the database and the plc using Snap7-python comunication methode.

Serial input:

- Checks if the arduino is started up correctly
- When a new order is dedected and what the tag id is of that case for the order
- When an order is detected in the procces and where

Serial output:

- The tracking id linked to the new order

Snap-7 Outputs:

- Updates the current location to the plc

## PLC.py

Comunicates between the Siemens PLC and the database using Snap7-python communication methode.

Snap-7 inputs:

- Checks if the PLC is started up and is running correctly
- Checks if the PLC is ready for a new order

Snap-7 Outputs:

- Upload the active* order to the plc


*not finished or not started order