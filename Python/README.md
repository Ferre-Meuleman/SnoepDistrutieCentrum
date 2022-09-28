# Snoep distributiecentrum
Eindwerk van het middelbaar gemaakt in 
TSM Mechelen
2021-2022 6EM
## Doel van het project
Aan de hand van RFID je bestelling snoep kunnen volgen doorheen het snoepdistributiecentrum en deze vervolgens weergeven op een web pagina.
## Logica
1. Gebruiker plaatst bestelling op website   
2. Word opgelsagen in database (json map)  
3. Indien plc opgestart en klaar voor bestelling word deze geupload naar de plc
4. Plc start bestelling (groot of klein bakje)
5. indine bakje voor 1ste RFID module kom
6. Tag word leeg gemaakt en nieuwe bestelling uit database word hierop weg geschreven
7. Website word geupdate dat de bestelling in het procces zit en de tag id + locatie word geupdate op plc
8. Besteling komt voorbij 2de rfid module 
9. Website word geupdate met de locatie + locatie word geupdate op plc
10. ...
