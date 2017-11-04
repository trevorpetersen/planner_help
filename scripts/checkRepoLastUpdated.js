"use strict"
var request = require("request");
var fs = require('fs');

let url = "https://api.github.com/repos/trevorpetersen/planner_help";
let lastUpdatedFileName = "last_updated";


let newUpdateTime = getNewUpdateTime();
let oldUpdateTime = getOldUpdateTime();

Promise.all([oldUpdateTime, newUpdateTime]).then(function(data){
  let oldUpdate = data[0];
  let newUpdate = data[1];

  if(oldUpdate != newUpdate){
    overwriteFile(newUpdate);
    console.log(1);
    return;
  }
  console.log(0);

})

.catch(function(error){
  console.log(-1);
});


function getOldUpdateTime(){
  return new Promise(function(resolve, reject){

    fs.readFile(lastUpdatedFileName, 'utf8', function (err,data) {
      if (err) {
        resolve(null);
      }
      resolve(data);
    });

  });
}

function getNewUpdateTime(){
  let userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1";

  let headers = {
    "User-agent": userAgent
  }
  let requestObj = {
    url: url,
    json: true,
    headers: headers
  }

  return new Promise(function(resolve, reject){
    request(requestObj, function (error, response, body) {
      if(error){
        reject(error);
      }

      let repoObject = body;

      if(repoObject.updated_at == null){
        reject("JSON response has not \"updated_at\" field");
      }
      resolve(repoObject.updated_at)
    });
  });
}

function overwriteFile(newFileContents){
  fs.truncate(lastUpdatedFileName, 0, function() {
    fs.writeFile(lastUpdatedFileName, newFileContents, function (err) {
      if (err) {
        // Handle error
      }
    });
  });
}
