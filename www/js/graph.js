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

  // Sometimes one professor teaches multiple sections. We only want 1 bar graph
  let seen = {};
  for(let i = 0; i < sectionArray.length; i++){
    let currentSection = sectionArray[i];

    if(seen[currentSection.professor] == true){
      continue;
    }

    let bar = document.createElement("div");
    let barText = document.createElement("p");

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

    barText.classList.add("barText");

    let classInfo = currentSection.name + "</br>";
    let gpaInfo = currentSection.professor + ": " + avgGrade + " (" + GPAToLetterGrade(avgGrade) + ")";
    let info = classInfo + gpaInfo;

    barText.innerHTML = info;
    $(bar).css("width", width + "%");

    bar.appendChild(barText);
    graphContainer.appendChild(bar);

    seen[currentSection.professor] = true;
  }
}

function setControls(courses){
  for(let i = 0; i < courses.length; i++){
    let course = courses[i];
    let button = document.createElement("button");
    let color = user.getColorByID(course.id);
    button.classList.add("graph-button");

    $(button).css("border", "solid 1px " + color);
    $(button).css("color", "black");
    $(button).css("borderRadius", "3px");
    $(button).css("backgroundColor", color);
    $(button).css("margin-left", "5px");

    //Select the first button
    if(i == 0){
      $(button).css("opacity","1")
    }

    button.onclick = function(){
      $(".graph-button").css("opacity","")
      $(this).css("opacity","1")
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
