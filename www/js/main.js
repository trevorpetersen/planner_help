var user = {};
user.courses = [];

var currentClasses;
var displayedClassNum;
var graphColors = ['blue', 'red', 'green', 'pink', 'orange', 'purple', 'black'];

//TODO Handle blank input, input that is not a class
$(document).ready(function(){
  hideTabs();

  addClassInput('math 109');
  addClassInput('chem 100a');
  //addClassInput('phil 27');
  //addClassInput('phil 28');

  hideCalendar();
  createCalendar();
  createBarGraph("Createive title",["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],[12, 19, 3, 5, 2, 3]);

  showTab('GEN-data');
});

function createBarGraph(title, labels, data){
  var ctx = document.getElementById("gpa-bar-graph").getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: labels,
        datasets: [{
            label: title,
            data: data,
            backgroundColor: graphColors,
            borderColor: graphColors,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});


}

function addClassInput(val){
  let newInput = createClassInput(val);
  document.getElementById("class-input-holder").appendChild(newInput);
}

function createClassInput(val){
  let container = document.createElement("div");
  container.classList.add('input-container')

  let label = document.createElement("p");
  label.classList.add('text-muted');
  label.innerHTML = "Choose Class: ";

  let row = document.createElement("div");
  //row.classList.add('row');
  row.classList.add('input-row');


  let col1 = document.createElement('div');
  col1.classList.add('col');

  let col2 = document.createElement('div');
  col2.classList.add('col');

  let input = document.createElement("input");
  input.classList.add('form-control');
  input.classList.add('class-input');
  input.value = val;
  input.placeholder = "Class Code";

  let removeButton = document.createElement('button');
  removeButton.classList.add('btn');
  removeButton.classList.add('btn-outline-danger');
  removeButton.innerHTML = 'X';
  removeButton.onclick = function(){
    container.parentNode.removeChild(container);
  }

  let searchSuggestion = document.createElement('div');
  searchSuggestion.classList.add('searchSuggestionBox');

  col1.appendChild(input);
  col2.appendChild(removeButton);

  //row.appendChild(col1);
  //row.appendChild(col2);

  row.appendChild(input);
  row.appendChild(removeButton);

  container.appendChild(label);
  container.appendChild(row);
  container.appendChild(searchSuggestion);

  $(input).on('input',function(e){
    let inputText = e.target.value;
    let searchSuggestion = $(e.target.parentNode.parentNode).find('.searchSuggestionBox')[0];

    if(inputText == ""){
      searchSuggestion.innerHTML = "";
      $(searchSuggestion).hide();
      return;
    }

    getClassSuggestions(inputText).then(function(wordArray){
      $(searchSuggestion).empty();
      wordArray.forEach(function(word){
        let suggestionItem = document.createElement("p");
        suggestionItem.innerHTML = word;
        $(suggestionItem).addClass("search_suggestion_item");
        $(suggestionItem).click(function(){
          onSuggestionClicked(this, e.target)
        });

        searchSuggestion.appendChild(suggestionItem);
      });

      if(searchSuggestion.innerHTML == ""){
        $(searchSuggestion).hide();
      }else{
        $(searchSuggestion).show();
      }
    })

  });

  $(input).blur(function() {
    setTimeout(function(){$(searchSuggestion).hide()}, 50);
  });

  return container;
}

function onSuggestionClicked(clickedElement, searchInput){
  searchInput.value = clickedElement.innerHTML;
}

function displayResults(){
  resetCalendar();
  getDataOnAllClasses().then(function(classesArray){
    let validCombos = generateSchedules(classesArray);
    currentClasses = validCombos;

    console.log(classesArray);
    user.courses = classesArray;
    for(let i = 0; i < classesArray.length; i++){
       let course = classesArray[i];
       let courseObj = {};
       if(course[0] != null){
         courseObj.name = course[0].name;
       }else{
         courseObj.name = null;
       }
       courseObj.sections = course;
      // user.courses.push(courseObj);
    }

    if(validCombos.length > 0){
      showCalendar();
      window.location.hash = "#cal";
      //TODO Better next line
      history.pushState("", document.title, window.location.pathname);
      displayedClassNum = 0;
      let combo = validCombos[displayedClassNum];
      highlightClasses(combo);
      document.getElementById("currentCourseNum").innerHTML = displayedClassNum + 1;
      document.getElementById("maxCourseNum").innerHTML = validCombos.length;
    }

    getCapeObjects(classesArray).then(function(obj){
      obj.forEach(x=> console.log( getCourseWithBestGPA(x.capes)))
    })
  });
}

function generateSchedules(classesArray){
  if($('.class-input').length == 0){
    hideCalendar();
    return;
  }
  let combos = cartesian(classesArray);
  console.log(combos.length);

  let validCombos = new Array();
  for(let i = 0; i < combos.length; i++){
    let combo = combos[i];
    let valid = true;

    for(let j = 0; j < combo.length; j++){
      for(let k = j + 1; k < combo.length; k++){

        if(overlaps(combo[j], combo[k])){
          valid = false;
        }
      }
    }
    if(valid){
      validCombos.push(combo);
    }
  }
  console.log(validCombos.length);
  return validCombos;
}

function cartesian(arg) {
    var r = [], arg = arg, max = arg.length-1;
    function helper(arr, i) {
        for (var j=0, l=arg[i].length; j<l; j++) {
            var a = arr.slice(0); // clone arr
            a.push(arg[i][j]);
            if (i==max)
                r.push(a);
            else
                helper(a, i+1);
        }
    }
    helper([], 0);
    return r;
}

function getDataOnAllClasses(){
  let promises = new Array();
  let allClasses = $('.class-input');
  console.log(allClasses);
  for(let i = 0; i < allClasses.length; i++){
    let classInput = allClasses[i];
    let promise = getDataOnClass(classInput.value);
    promises.push(promise)
  }
  return Promise.all(promises);
}

function getDataOnClass(className){
  let coursesArray;
  let capesArray;


  return getCurrentClasses(className);

/*
    .then(function(courses){
      console.log(courses)
      setTitles(courses, className)
      coursesArray = courses;
      if(courses.length == 0){
        console.log('No courses');
        return Promise.resolve(null)
      }
      return getCapes(courses, className);
    })
    .then(function(capes){
      capesArray = capes;
      let courseBundles = bundleCoursesAndCapes(coursesArray,capesArray);
      resolve(courseBundles);
    })
    .catch(function(error){
      console.log(error);
      reject(null);
    })
*/
}

function switchTab(obj){
  switch (obj.id) {
    case 'GEN':
      hideTabs();
      showTab(obj.id + '-data');
      break;

    case 'GPA':
      hideTabs();
      showTab(obj.id + '-data');
      break;
  }
}

function hideTabs(){
  $('.tab-data').hide();
}

function showTab(id){
  $('#' + id).show();
}

function bundleCoursesAndCapes(courses, capes){
  let courseBundles = new Array();
  for(let i = 0; i < courses.length; i++){
    let bundle = new Object();
    bundle.course = courses[i];
    bundle.capes = capes[i];
    bundle.name = courses[i].title;

    courseBundles.push(bundle);
  }
  return courseBundles;
}

function setTitles(courses, className){
  for(let i = 0; i < courses.length; i++){
    courses[i].title = className;
  }
}

function combineArrays(arrayOfArrays){
  let returnArray = [];

  for(let i = 0; i < arrayOfArrays.length; i++){
    let currentArray = arrayOfArrays[i];
    for(let j= 0; j < currentArray.length; j++){
      returnArray.push(currentArray[j]);
    }
  }
  return returnArray;
}

function removeEmptyArrays(arrayOfArrays){
  for(let i = 0; i < arrayOfArrays.length; i++){
    if(arrayOfArrays[i].length == 0){
      arrayOfArrays.splice(i, 1);
    }
  }
}

function getCapeObjects(classesArrayofArrays){
  let capePromises = [];
  for(let i = 0; i < classesArrayofArrays.length; i++){
    let arrayOfCourses = classesArrayofArrays[i];
    capePromises.push(getCapes(arrayOfCourses));
  }

  return Promise.all(capePromises).then(function(arrayOfCapeArrays){
    let capeObjects = [];
    for(let i = 0; i < classesArrayofArrays.length; i++){
      let capeObject = {};
      capeObject.capes = arrayOfCapeArrays[i];
      capeObject.course_name = classesArrayofArrays[i][0].name;

      capeObjects.push(capeObject);
    }
    return Promise.resolve(capeObjects);
  });
}

function getCapes(courses){
  let capesRequests = new Array();
  for( let i = 0; i < courses.length; i ++){
    console.log(courses[i].professor, courses[i].name);
    capesRequests.push(getCape(courses[i].professor, courses[i].name));
  }

  return Promise.all(capesRequests).then(function(capesArrayofArrays){
    removeEmptyArrays(capesArrayofArrays);
    return Promise.resolve(capesArrayofArrays);
  });
}

function getClassSuggestions(userText){
  return new Promise(function(resolve, reject){
    $.post("getClassSuggestions",{userText:userText}).then(function(data){
        resolve(data);
      });
  })
}

function getCape(professorName, className){
  return new Promise(function(resolve, reject){
    $.post("getCapes",{classname:className, professor:professorName}).then(function(data){
      resolve(data);
    });
  });
}

function getCurrentClasses(className){
  return new Promise(function(resolve, reject){
    $.post("getCurrentClasses",{classname:className}).then(function(data){
      resolve(data);
    })

    .catch(function(error){
      console.log("Error in getCurrentClasses");
      reject(error);
    });
  });

}

function getIndexOfMaxGPA(gpas){
  let max = gpas[0];
  let index = 0;
  for(let i = 1; i < gpas.length; i++){
    if(gpas[i] > max){
      max = gpas[i];
      index = i;
    }
  }
  return index;
}

function getGPAs(capes){
  gpas = new Array();
  for(let i = 0; i < capes.length; i++){
    let sum = 0;
    let num = 0;
    for(let j = 0; j < capes[i].length; j++){
      gpa = parseGPA(capes[i][j]["avg_grade_expected"]);
      if(! isNaN(gpa)){
        sum += gpa;
        num += 1;
      }
    }
    if(num != 0){
      gpas.push((sum/num));
    }else{
      gpas.push(0);
    }
  }
  return gpas;
}

function parseGPA(gpaString){
  if(! gpaString.includes("(")){
    return parseFloat(gpaString);
  }else{
    gpaString = gpaString.substring(gpaString.indexOf("(") + 1);
    gpaString = gpaString.substring(0,gpaString.length - 1);
    return parseFloat(gpaString);
  }
}

function getCourseWithBestGPA(capes){
  if(capes.length == 0){
    return null;
  }
  let gpas = getGPAs(capes);
  let maxIndex = getIndexOfMaxGPA(gpas);

  let best = new Object();
  best.professor = capes[maxIndex][0]['instructor'];
  best.gpa = gpas[maxIndex];
  return best;
}

function overlaps(course1, course2){
  for(let i = 0; i < course1.meetings.length; i++){
    let meeting1 = course1.meetings[i];
    for(let j = 0; j < course2.meetings.length; j++){
      let meeting2 = course2.meetings[j];

      if(meetingsOverlap(meeting1, meeting2)){
        return true;
      }
    }
  }
  return false;
}

function meetingsOverlap(meeting1, meeting2){
  let overlaps = false;

  for(let i = 0; i < meeting1.time.length; i++){
    let start1 = meeting1.time[i][0];
    let end1 = meeting1.time[i][1];

    for(let j = 0; j < meeting2.time.length; j++){

      let start2 = meeting2.time[j][0];
      let end2 = meeting2.time[j][1];

      if(start1 == start2 || (start1 < start2 && end1 > start2)){
          overlaps = true;
      }
    }
  }
  return overlaps;
}
