function createGraph(courses){
  if(courses.length > 0){
    createBars(courses[0]);
    setControls(courses);
  }else{
    // TODO There are not courses
  }
}

function setGraph(course){
  clearBars();
  createBars(course);
}

function createBars(course){

  let sectionArray = course.sections;
  let graphContainer = document.getElementById("graph-container");

  sectionArray.sort(function(a,b){return b.averageGrade - a.averageGrade});

  for(let i = 0; i < sectionArray.length; i++){
    let bar = document.createElement("div");
    let currentSection = sectionArray[i];

    let width;
    if(currentSection.averageGrade != 0){
      width = (currentSection.averageGrade / 4) * 100;
    }else{
      width = 100;
      $(bar).css("opacity", .5);
    }

    let avgGrade = currentSection.averageGrade;
    bar.classList.add("bar");
    bar.classList.add("styled-box");
    bar.classList.add("selected-color-" + course.id);

    let classInfo = currentSection.name + "</br>";
    let gpaInfo = currentSection.professor + ": " + avgGrade + " (" + GPAToLetterGrade(avgGrade) + ")";
    let info = classInfo + gpaInfo;

    bar.innerHTML = info;
    $(bar).css("width", width + "%");
    graphContainer.appendChild(bar);

  }
}

function setControls(courses){
  for(let i = 0; i < courses.length; i++){
    let course = courses[i];
    let button = document.createElement("button");
    let color = user.getColorByID(course.id);

    $(button).css("border", "solid 1px " + color);
    $(button).css("color", "black");
    $(button).css("borderRadius", "3px");
    $(button).css("backgroundColor", color);
    $(button).css("margin-left", "5px");

    button.onclick = function(){
      setGraph(course);
    }
    button.innerHTML = course.name;

    document.getElementById('graph-controls').appendChild(button);
  }
}

function clearBars(){
  $('#graph-container').empty();
}

function clearControls(){
  $('#graph-controls').empty();
}

function resetGraph(){
  clearBars();
  clearControls();
}
