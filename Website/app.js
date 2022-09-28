const express = require("express");
const bodyParser = require("body-parser")
const fs = require('fs');
const ejs = require('ejs');
const path = require('path');
let alert = require('alert');

// Server
const app = express();
app.use(bodyParser.urlencoded({
    extended: true
}));

app.set("view engine", "ejs");

//index.html laden bij request
app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html");
    app.use(express.static(__dirname));
});
//index.html laden bij request
app.get("/index.html", function(req, res) {
    res.sendFile(__dirname + "/index.html");
    app.use(express.static(__dirname));
});
//index.html laden bij request
app.get("/Order.html", function(req, res) {
    res.sendFile(__dirname + "/Order.html");
    app.use(express.static(__dirname));
});

//Tracking.html laden bij request
app.get("/Tracking.html", function(req, res) {
    res.render('Tracking', {
        data: "",
        Firstname: "",
        Lastname: "",
        Rood: "",
        Groen: "",
        Blauw: "",
        TrackingID: "",
        CardID: "",
        Location: 0
    });
})
//lege tracking pagina laden
app.get("/Tracking", function(req, res) {
    res.render('Tracking', {
        data: "",
        Firstname: "",
        Lastname: "",
        Rood: "",
        Groen: "",
        Blauw: "",
        TrackingID: "",
        CardID: "",
        Location: 0
    });
})

//websit op ip poort 3000 laten lopen
app.listen(3000, function() {
    console.log("server is running on port 3000");
})

//tracking id pagina laden als tracking code is ingevuld
app.post("/Tracking", function(req, res) {
    var TrackingID = String(req.body.search);
    var IDs = getIDs();

    if (IDs.includes(TrackingID)) {
        var i = IDs.indexOf(TrackingID);
        var orderdata = search(i);
        res.render('Tracking', {
            data: "U bestelling:",
            Firstname: orderdata.FirstName,
            Lastname: orderdata.Lastname,
            Rood: orderdata.R,
            Groen: orderdata.G,
            Blauw: orderdata.B,
            TrackingID: orderdata.TrackingID,
            CardID: orderdata.CardID,
            Location: orderdata.Location
        });

    } else {
        res.render('Tracking', {
            data: "De tracking code is niet inorde",
            Firstname: "",
            Lastname: "",
            Rood: "",
            Groen: "",
            Blauw: "",
            TrackingID: "",
            CardID: "",
            Location: 0
        });
    }

});

//fucntie voor besteling te zoeken zoeken in de orders map
function search(i) {
    var file = '../Json/orders/order' + (i + 1) + '.Json';
    var data = fs.readFileSync(file);
    var obj = JSON.parse(data);
    var orderdata = {
        orderID: obj.orderID,
        FirstName: obj.FirstName,
        Lastname: obj.LastName,
        R: obj.R,
        G: obj.G,
        B: obj.B,
        Big_Small: obj.Big_Small,
        Location: obj.Location,
        CardID: obj.CardID,
        TrackingID: obj.TrackingID
    };

    return orderdata;
}

//order form to json file
app.post("/orderform", function(req, res) {

    // Data uit html form:
    var Firstname = String(req.body.Firstname);
    var Lastname = String(req.body.Lastname);
    var Rood = Number(req.body.Rood);
    var Groen = Number(req.body.Groen);
    var Blauw = Number(req.body.Blauw);

    // Data uit andere functies:
    var TrackingID = makeid(6);
    var ordernum = newnum() + 1;

    var number = Number(Rood + Groen + Blauw);
    var Big_Small = Number(0);
    if (number > 8) {

    } else if (number > 4) {
        Big_Small = 1;
    }


    // onbepaalde data:
    var Location = 0;
    var CardID = '';



    // Data in Json klaarzetten:
    var order = {
        orderID: ordernum,
        FirstName: Firstname,
        LastName: Lastname,
        R: Rood,
        G: Groen,
        B: Blauw,
        Big_Small: Big_Small,
        Location: Location,
        CardID: CardID,
        TrackingID: TrackingID
    };

    // Data omzetten naar stirng :
    var jsonString = JSON.stringify(order, null, 4);

    // Path bepalen voor nieuwe json order file:
    var orderpath = '../Json/orders' + '/order' + ordernum + '.json';

    // Json file schrijven + openen TrackingCode page
    fs.writeFile(orderpath, jsonString, err => {
        if (err) {
            console.log('Error writing file', err);
        } else {
            console.log('Successfully wrote file', orderpath);
            res.render('TrackingCode', { data: TrackingID });
        }
    });
});

// Functie voor unieke tracking id:
function makeid(length) {
    var ids = getIDs();
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() *
            charactersLength));
    }

    while (ids.includes(result)) {
        for (var i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() *
                charactersLength));
        }
    }
    return result;
}


// list maken van alle TrackingID's
function getIDs() {
    var IDs = [];
    var files = fs.readdirSync('../Json/orders');
    for (var i = 1; i < files.length + 1; i++) {
        var file = '../Json/orders/order' + i + '.Json'
        var data = fs.readFileSync(file);
        var obj = JSON.parse(data);
        var ID = obj.TrackingID;
        IDs.push(String(ID));

    }
    return IDs
}


// Functie bepalen aantal orders:
function newnum() {
    var files = fs.readdirSync('../Json/orders');
    var num = files.length;
    return num;
}
