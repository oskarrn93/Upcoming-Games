
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/upcoming";

var express = require('express');
var cors = require('cors');
var app = express();
 
app.use(cors());
 
app.get('/cs', function (req, res) {
    getUpcomingCs(function(result) {
        console.log("result");
        console.log(result);
        res.send(result);
    });
})

app.get('/fotball', function (req, res) {
    getUpcomingFotball(function(result) {
        console.log("result");
        console.log(result);
        res.send(result);
    });
})

app.listen(8001, function () {
  console.log('CORS-enabled web server listening on port 8001')
})


function getUpcomingCs(callback) {
     MongoClient.connect(url, function(err, db) {
        if (err) 
            throw err;
        db.collection("cs").find({}).toArray(function(err, result) {
            if (err) 
                throw err;
            callback(result);
            db.close();
        });
    });
}

function getUpcomingFotball(callback) {
     MongoClient.connect(url, function(err, db) {
        if (err) 
            throw err;
        db.collection("fotball").find({}).toArray(function(err, result) {
            if (err) 
                throw err;
            callback(result);
            db.close();
        });
    });
}