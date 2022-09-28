/**
   --------------------------------------------------------------------------------------------------------------------
   Example sketch/program showing how to read data from more than one PICC to serial.
   --------------------------------------------------------------------------------------------------------------------
   This is a mfrc522[reader] library example; for further details and other examples see: https://github.com/miguelbalboa/rfid

   Example sketch/program showing how to read data from more than one PICC (that is: a RFID Tag or Card) using a
   mfrc522[reader] based RFID Reader on the Arduino SPI interface.

   Warning: This may not work! Multiple devices at one SPI are difficult and cause many trouble!! Engineering skill
            and knowledge are required!

   @license Released into the public domain.

   Typical pin layout used:
   ------------------------------------
               mfrc522[reader]      
               Reader/PCD   Uno/101    
   Signal      Pin          Pin        
   ------------------------------------
   RST/Reset   RST          9          
   SPI SS 1    SDA(SS1)     10 
   SPI SS 2    SDA(SS2)     8 
   SPI SS 3    SDA(SS3)     7 
   SPI SS 4    SDA(SS4)     6 
   SPI MOSI    MOSI         11 / ICSP-4
   SPI MISO    MISO         12 / ICSP-1
   SPI SCK     SCK          13 / ICSP-3   

*/

//nodige extensies
#include <Wire.h>
#include <SPI.h>
#include <MFRC522.h>

//pin output
#define RST_PIN 9
#define SS_1_PIN 10
#define SS_2_PIN 8
#define SS_3_PIN 7
#define SS_4_PIN 6

//aantal readers
#define NR_OF_READERS 4

//volgorde van scanners
byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN, SS_4_PIN};

//
MFRC522 mfrc522[NR_OF_READERS]; 
int i = 1;
byte code[10];
int counter[NR_OF_READERS] = {0, 0};
String uidString;

//alles wat de arduino 1 keer moet uitvoeren
void setup()
{
  Serial.begin(9600);
  while (!Serial);
  SPI.begin(); 

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++)
  {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN);
    mfrc522[reader].PCD_Init();
    Serial.print(F("Startup "));
    Serial.print(reader);
    Serial.print(F(": "));
    mfrc522[reader].PCD_DumpVersionToSerial();
  }
}

uint8_t control = 0x00;

//alles wat de arduino constant uitvoerd
void loop()
{
  MFRC522::MIFARE_Key key;
  for (byte i = 0; i < 6; i++)
    key.keyByte[i] = 0xFF;

  byte block;
  byte len;
  MFRC522::StatusCode status;

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++)
  {

    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial())
    {
      //als de eerste schanner dedecteerd vraag aan de seriele monitor naam van actieve bestelling
      if (reader == 0)
      {
        Serial.print("Reader ");
        Serial.print(reader);
        Serial.print(": ");
        dump_byte_array(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
        Serial.println();
        byte buffer[34];
        byte block;
        MFRC522::StatusCode status;
        byte len;

        Serial.setTimeout(2000L);

        len = Serial.readBytesUntil('#', (char *)buffer, 20);
        for (byte i = len; i < 20; i++)
          buffer[i] = ' '; 

        block = 4;

        status = mfrc522[reader].PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522[reader].uid));
        if (status != MFRC522::STATUS_OK)
        {
          Serial.print(F("PCD_Authenticate() failed: "));
          Serial.print(mfrc522[reader].GetStatusCodeName(status));
          Serial.println();
          return;
        }


        status = mfrc522[reader].MIFARE_Write(block, buffer, 16);
        if (status != MFRC522::STATUS_OK)
        {
          Serial.print(F("MIFARE_Write() failed: "));
          Serial.print(mfrc522[reader].GetStatusCodeName(status));
          Serial.println();

          return;
        }

        block = 5;

        status = mfrc522[reader].PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522[reader].uid));
        if (status != MFRC522::STATUS_OK)
        {
          Serial.print(F("PCD_Authenticate() failed: "));
          Serial.print(mfrc522[reader].GetStatusCodeName(status));
          Serial.println();

          return;
        }


        status = mfrc522[reader].MIFARE_Write(block, &buffer[16], 16);
        if (status != MFRC522::STATUS_OK)
        {
          Serial.print(F("MIFARE_Write() failed: "));
          Serial.print(mfrc522[reader].GetStatusCodeName(status));
          Serial.println();
          return;

        }
        else
          Serial.print(F("MIFARE_Write() success: "));
          Serial.println();

      }
      //als scanner niet de eerste is lees welke bestelling en verhoog de locatie
      if (reader != 0)
      {
        byte buffer1[18];
        block = 4;
        len = 18;

        status = mfrc522[reader].PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 4, &key, &(mfrc522[reader].uid)); // line 834 of MFRC522.cpp file
        if (status != MFRC522::STATUS_OK)
        {
          Serial.print(F("Authentication failed: "));
          Serial.println(mfrc522[reader].GetStatusCodeName(status));
          return;
        }

        status = mfrc522[reader].MIFARE_Read(block, buffer1, &len);
        if (status != MFRC522::STATUS_OK)
        {
          Serial.print(F("Reading failed: "));
          Serial.println(mfrc522[reader].GetStatusCodeName(status));
          return;
        }
        String value = "";
        for (uint8_t i = 0; i < 16; i++)
        {
          if (buffer1[i] != 32)
          {
            value += (char)buffer1[i];
          }
        }
        Serial.print("Reader ");
        Serial.print(reader);
        Serial.print(": ");
        dump_byte_array(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
        Serial.print(", ");
        value.trim();
        Serial.print(value);
        Serial.println();
      }
    }
    delay(50);
    mfrc522[reader].PICC_HaltA();
    mfrc522[reader].PCD_StopCrypto1();
  }
}

//functie om bytes uit te lezen
void dump_byte_array(byte *buffer, byte bufferSize)
{
  String value = "";
  for (byte i = 0; i < bufferSize; i++)
  {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}