# C++ [more like .ino files :)]

C++ becouse Arduino run's on a version of c++

## ~/Arduino/Arduino.ino

I used .ino file to program my arduino to comunicate with the RFID modules and[] to the central system(main.py ran on pc).
For the communication between the Arduino and the RFID modules im using SPI.

SPI input:

- When a new order is dedected and what the tag id is of that case for the order
- What module dedected a order and what the orders data is

SPI output:

- The trachking id linked to the new order

For the communication between the Arduio and the central System imusing Serial.
Serial input:

- The tracking id linked to the new order

Serial output:

- if the arduino is started up correctly sends a signal
- When a new order is dedected and what the tag id is of that case for the order
- When an order is detected in the procces and where

## ~/MFRC522/...

This folder is the modified library for the Arduino MFRC522 RFID modules. The only thing i changed is the the Communication frequenctie to use the spi communication over longer distances (±10m).
