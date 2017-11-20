function createGraph(courses){
  for(let i = 0; i < courses.length; i++){
    createBar(courses[i].sections);
  }
}

function createBar(sectionArray){
  let graphContainer = document.getElementById("graph-container");

  sectionArray.sort(function(a,b){return b.averageGrade - a.averageGrade});
  console.log(sectionArray);

  for(let i = 0; i < sectionArray.length; i++){
    let bar1 = document.createElement("div");
    let currentSection = sectionArray[i];

    let width;
    if(currentSection.averageGrade != 0){
      width = (currentSection.averageGrade / 4) * 100;
    }else{
      width = 100;
      $(bar1).css("background-color", "gray");
      $(bar1).css("opacity", .5);
      $(bar1).css("border", "gray");
    }

    bar1.classList.add("bar");
    bar1.innerHTML = currentSection.professor + ":" + currentSection.averageGrade;
    $(bar1).css("width", width + "%");

    graphContainer.appendChild(bar1);

  }




}
