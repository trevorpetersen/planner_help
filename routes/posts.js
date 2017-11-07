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
    returnJSON(res, wordArray);
  });
});

router.post(GET_CAPES, function(req, res, next){
  if(incorrectPostData(req.url, req.body)){
    handleBadPostData(next);
    return;
  }

  let className = req.body.classname;
  let professorName = req.body.professor;

  getCapes(className, professorName)
  .then(function(capesArray){
    returnJSON(res, capesArray);
  })

  .catch(function(){
    // TODO Handle error while getting capes
  });
});

router.post(GET_CLASSES, function(req, res, next){
  if(incorrectPostData(req.url, req.body)){
    handleBadPostData(next);
    return;
  }
  let className = req.body.classname;
  getClasses(className).then(function(classes){
    returnJSON(res, classes)
  })
  .catch(function(error){
    res.statusCode = 500;
    res.send();
  });
});

function getCapes(className, professorName){
  return sql.getCapes(className, professorName)
  .then(function(data){
    return Promise.resolve(data);
  })
}

function getClasses(className){
  return new Promise(function(resolve, reject){
    sql.getClasses(className)

    .then(function(classes){
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

  .catch(function(err){
    console.log(err)
  })

}

function returnJSON(res, data){
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json');
  res.send(JSON.stringify(data));
}

function handleBadPostData(next){
  var error = new Error('Bad Request');
  error.status = 400;
  next(error);
}

module.exports = router;
