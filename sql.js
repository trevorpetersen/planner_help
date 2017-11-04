"use strict"
var mysql = require('mysql');
var myClasses = require('./classes');
var exports = module.exports = {};

var con = mysql.createConnection({
  host: config.sql.host,
  user: config.sql.username,
  password: config.sql.password,
  database: config.sql.database
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});


exports.getClasses = function(className){
  return new Promise(function(resolve, reject){
    query = "SELECT * from current_classes where CLASS_NAME LIKE ? and (FK_SPM_SPCL_MTG_CD is NULL)";
    con.query(query,[className], function (err, result, fields) {
      if (err){
        reject(err);
      }else{
        let classes = createClassesFromQueryResults(result);
        resolve(classes);
      }
    });
  })
};

exports.getMatchingClasses = function(userText){
  return new Promise(function(resolve, reject){
    query = "SELECT * from course_catalog where course_name LIKE ?";
    con.query(query,["%" + userText + "%"], function (err, result, fields) {
      if (err){
        reject(err);
      }else{
        let courseNames = result.map(x => x.course_name);
        courseNames = getBestMatches(userText, courseNames, 5);

        resolve(courseNames);
      }
    });
  })
}

function getBestMatches(queryString, classArray, maxNum){
  queryString = queryString.toUpperCase();
  let bestMatches = [];
  let okMatches = [];

  for(let i = 0; i < classArray.length; i++){
    let currentClass = classArray[i].toUpperCase();
    if(currentClass.indexOf(queryString) == 0){
      console.log("Found best match: " + currentClass);
      bestMatches.push(currentClass);
    }else{
      okMatches.push(currentClass);
    }

  }

  let sortedMatches = [];

  for(let i = 0; i < bestMatches.length; i++){
    sortedMatches.push(bestMatches[i]);
  }
  for(let i = 0; i < okMatches.length; i++){
    sortedMatches.push(okMatches[i]);
  }

  if(sortedMatches.length <= maxNum){
    return sortedMatches;
  }else{
    return sortedMatches.splice(0, maxNum);
  }

}

function createClassesFromQueryResults(result){
  let lectures = getLecturesFromResults(result);
  let discussions = getDiscussionsFromResults(result);
  let courses = new Array();
  for(let i = 0; i < lectures.length; i++){
    let lecture = lectures[i];

    let name = lecture['CLASS_NAME'];
    let sectionCode = lecture['SECT_CODE'];
    let dayCode = lecture['DAY_CODE'];
    let beginH = lecture['BEGIN_HH_TIME'];
    let beginM = lecture['BEGIN_MM_TIME'];
    let endH = lecture['END_HH_TIME'];
    let endM = lecture['END_MM_TIME'];

    let meeting = new myClasses.Meeting(dayCode, beginH, beginM, endH, endM);

    let course = null;
    for(let j = 0; j < courses.length; j++){
      let current = courses[j];
      if(current.sectionCode == sectionCode){
        course = current;
        break;
      }
    }

    if(course == null){
      course = new myClasses.Course(name, sectionCode);
      courses.push(course);
    }

    course.addMeeting(meeting)

    for(let j = 0; j < discussions.length; j++){
      let discussion = discussions[j];

      let name = discussion['CLASS_NAME'];
      let sectionCode = discussion['SECT_CODE'];
      let dayCode = discussion['DAY_CODE'];
      let beginH = discussion['BEGIN_HH_TIME'];
      let beginM = discussion['BEGIN_MM_TIME'];
      let endH = discussion['END_HH_TIME'];
      let endM = discussion['END_MM_TIME'];

      let myDiscussion  = new myClasses.Course(name, sectionCode);
      let meeting = new myClasses.Meeting(dayCode, beginH, beginM, endH, endM);

      myDiscussion.addMeeting(meeting);

      if(course.sectionCode.charAt(0) == discussion['SECT_CODE'].charAt(0)){
        course.addDiscussion(myDiscussion);
      }
    }
  }

  return courses;
}

function getMatching(array, key, desiredValue){
  let returnValue = new Array();
  for(let i = 0; i < array.length; i++){
    let current = array[i];
    let type = current[key];
    if( type != null && type.toUpperCase().includes(desiredValue.toUpperCase())){
      returnValue.push(current);
    }
  }
  return returnValue;
}

function getNotMatching(array, key, desiredValue){
  let returnValue = new Array();
  for(let i = 0; i < array.length; i++){
    let current = array[i];
    let type = current[key];
    if( type != null && ! type.toUpperCase().includes(desiredValue.toUpperCase())){
      returnValue.push(current);
    }
  }
  return returnValue;
}

function getLecturesFromResults(result){
  return getMatching(result, 'FK_CDI_INSTR_TYPE', 'LE');
}

function getDiscussionsFromResults(result){
  return getNotMatching(result, 'FK_CDI_INSTR_TYPE', 'LE');
}
