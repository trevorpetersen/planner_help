"use strict"
var express = require('express');
var request = require('request');
var sql = require('../sql');

const GET_CAPES = '/getCapes';
const GET_CLASSES = '/getCurrentClasses';
const GET_CLASS_SUGGESTIONS = '/getClassSuggestions';



var router = express.Router();

router.post(GET_CLASS_SUGGESTIONS, function(req, res, next){
  if(incorrectPostData(req.url, req.body)){
    handleBadPostData(next);
    return;
  }

  let userText = req.body.userText;

  getClassSuggestions(userText).then(function(wordArray){
    //console.log(wordArray);
    res.statusCode = 200;
    res.send(JSON.stringify(wordArray));
  });
});

router.post(GET_CAPES, function(req, res, next){
  getCapes(req, res,next);
});

router.post(GET_CLASSES, function(req, res, next){
  if(incorrectPostData(req.url, req.body)){
    handleBadPostData(next);
    return;
  }
  className = req.body.classname;
  getClasses(className).then(function(classes){
    res.statusCode = 200;
    res.send(JSON.stringify(classes));
  })
  .catch(function(error){
    res.statusCode = 500;
    res.send();
  });
});

function getCapes(req, res, next){
  if(incorrectPostData(req.url, req.body)){
    handleBadPostData(next);
    return;
  }


  classname = req.body.classname;
  professorname = req.body.professor;

}

function getClasses(className){
  return new Promise(function(resolve, reject){
    sql.getClasses(className).then(function(classes){
      resolve(classes);
    })

    .catch(function(error){
      reject(error);
    });
  });
}

function incorrectPostData(endpoint, data){
  switch(endpoint){

    case GET_CAPES:
      return data.classname == undefined || data.professor == undefined;

    case GET_CLASSES:
      return data.classname == undefined;

    case GET_CLASS_SUGGESTIONS:
      return data.userText == undefined;

    default:
      console.log("Warning: No matching endpoint");
      return true;
  }
}

function getClassSuggestions(userText){
  return Promise.resolve()

  .then(function(){
    return sql.getMatchingClasses(userText);
  })

}

function handleBadPostData(next){
  var error = new Error('Bad Request');
  error.status = 400;
  next(error);
}

module.exports = router;
