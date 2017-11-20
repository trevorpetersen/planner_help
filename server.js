"use strict"

var config = require('./config');
var express = require('express');
var mysql = require('mysql');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var posts = require('./routes/posts');
var fs = require('fs');
var https = require('https');



var app = express();

var options = {
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
};

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(cookieParser());

app.use(express.static(__dirname + '/www'));
app.use('/', posts);
app.use(handlePageNotFound);
app.use(handleError)

https.createServer(options, app).listen(443);

app.listen(80, function(){
  console.log("Server is running on port 80");
});

function handlePageNotFound(req, res, next){
  var error = new Error('Not Found');
  error.status = 404;
  next(error);
}

function handleError(err, req, res, next){
  console.log("Error: " + err.status);
  console.log(req + "\n");
  return res.sendStatus(err.status);
}
