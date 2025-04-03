// load the things we need (this is all code from class)
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');
const {response} = require("express");

app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up an ejs view file

// initial login page
app.get('/', function(req, res) {

        //initial render without output
            res.render('login.ejs', {
            });
        });


app.post('/login', function(req, res){
   var storeduname = 'admin';
   var storedpswd = 'password';

   if (storeduname == req.body.uname && storedpswd == req.body.pswd)    // code pulled from class 9 ejs template
    {
        res.render('mainpage.ejs', {
            user : req.body.uname,
            auth : true
        });
    }
    else
    {
        res.render('mainpage.ejs', {
            user : 'unauthorized',
            auth : false
        });
    }
})

app.post('/redirect', function(req, res) {
    if (req.body.table == 'floor')
    {
        res.render('floor.ejs');
    }
    if (req.body.table == 'resident')
    {
        axios.get('http://127.0.0.1:5000/api/allroom', {headers: {'Content-Type': 'application/json'}})
            .then((response)=> {
            res.render('resident.ejs', {
                roomnum : response.data
            })
        });
    }
    if (req.body.table == 'room')
    {
        axios.get('http://127.0.0.1:5000/api/allfloor', {headers: {'Content-Type': 'application/json'}}).then(function (response) {
            res.render('room.ejs', {
                floornum : response.data
            })
        });
    }
})



app.post('/crud', function (req, res) {  //api calls using axios
    if (req.body.floor == 'create') {
        axios.post('http://127.0.0.1:5000/api/floor', {level: req.body.level, name: req.body.name})
            .then(function (response) {
                res.render('endpage.ejs', {  // render endpage with data to avoid empty options
                    create: response.data
                });
            })
    }
    if (req.body.floor == 'read') {
        axios.get('http://127.0.0.1:5000/api/floor', {
            headers: {'Content-Type': 'application/json'},  // needed to stop crash
            data: {level: req.body.level}
        })
            .then(function (response) {
                res.render('endpage.ejs', {
                    read_floor: true,
                    read: response.data
                });
            })
    }
    if (req.body.floor == 'update') {
        axios.put('http://127.0.0.1:5000/api/floor', {level: req.body.level, name: req.body.name})
            .then(function (response) {
                res.render('endpage.ejs', {
                    update: response.data
                });
            })
    }
    if (req.body.floor == 'delete') {
        axios.delete('http://127.0.0.1:5000/api/floor', {
            headers: {'Content-Type': 'application/json'},
            data: {level: req.body.level, name: req.body.name}
        })
            .then(function (response) {
                res.render('endpage.ejs', {
                    delete: response.data
                });
            })
    }
    if (req.body.resident == 'create') {
        axios.post('http://127.0.0.1:5000/api/resident', {
            firstname: req.body.firstname,
            lastname: req.body.lastname,
            age: req.body.age,
            room: req.body.room
        })
            .then(function (response) {
                res.render('endpage.ejs', {
                    create: response.data
                });
            })
    }
    if (req.body.resident == 'read') {
        axios.get('http://127.0.0.1:5000/api/resident', {
            headers: {'Content-Type': 'application/json'},
            data: {firstname: req.body.firstname, lastname: req.body.lastname}
        })
            .then(function (response) {
                res.render('endpage.ejs', {
                    read_res: true,
                    read: response.data
                });
            })
    }
    if (req.body.resident == 'update') {
        axios.put('http://127.0.0.1:5000/api/resident', {
            firstname: req.body.firstname,
            lastname: req.body.lastname,
            age: req.body.age
        })
            .then(function (response) {
                res.render('endpage.ejs', {
                    update: response.data
                });
            })
    }
    if (req.body.resident == 'delete') {
        axios.delete('http://127.0.0.1:5000/api/resident', {
            headers: {'Content-Type': 'application/json'},
            data: {firstname: req.body.firstname, lastname: req.body.lastname, age: req.body.age, room: req.body.room}
        })
            .then(function (response) {
                res.render('endpage.ejs', {
                    delete: response.data
                });
            })
    }
    if (req.body.room == 'create') {
        axios.post('http://127.0.0.1:5000/api/room', {
            capacity: req.body.capacity,
            number: req.body.number,
            floor: req.body.level
        })
            .then(function (response) {
                res.render('endpage.ejs', {
                    create: response.data
                });
            })
    }
    if (req.body.room == 'read') {
        axios.get('http://127.0.0.1:5000/api/room', {
            headers: {'Content-Type': 'application/json'},
            data: {number: req.body.number}
        })
            .then(function (response) {
                res.render('endpage.ejs', {
                    read_room: true,
                    read: response.data
                });
            })
    }
    if (req.body.room == 'update') {
        axios.put('http://127.0.0.1:5000/api/room', {number: req.body.number, old_number: req.body.old_number})
            .then(function (response) {
                res.render('endpage.ejs', {
                    update: response.data
                });
            })
    }
    if (req.body.room == 'delete') {
        axios.delete('http://127.0.0.1:5000/api/room', {
            headers: {'Content-Type': 'application/json'},
            data: {number : req.body.number, level : req.body.level}
        })
            .then(function (response) {
                res.render('endpage.ejs', {
                    delete: response.data
                });
            })
    }
})
// I based this on the code from homework 3, as well as w3schools tutorials.

app.listen(8080);
console.log('8080 is the magic port');
