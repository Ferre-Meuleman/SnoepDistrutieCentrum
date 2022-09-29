# Json

I use this folder as the "database" so save al my order and the active order.

## ~/orders/

In this folder is the placed orders are stored in Json files as order(ordernumber).
Json In this file there is all the data needed to process the order.
The data in these files is changed multiple times during this process.  
  
### This is an example file
```yaml
{
    "orderID": 1,
    "FirstName": "Your firsntame",
    "LastName": "Your lastname",
    "R": 1,
    "G": 0,
    "B": 0,
    "Big_Small": 0,
    "Location": 0,
    "CardID": "",
    "TrackingID": "vtjRoF"
}
```

## ~/Log/Log.Json

This file is used to save the active order its tracking id. 
