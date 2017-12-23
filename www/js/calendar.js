var colors = ['color-1', 'color-2', 'color-3', 'color-4', 'color-5', 'color-6', 'color-7', 'color-8'];
var colorIndex = 0;

function createCalendar(){
  let calDiv = document.getElementById('cal');
  let days = document.createElement('div');
  days.className += 'row';

  var dayString = [' ','Su','Mo','Tu','We','Th','Fr','Sa'];
  for(let i = 0; i < 8; i++){
    let day = document.createElement('div');
    day.classList.add('col');
    day.classList.add('text-muted');
    if(i != 0){
      day.classList.add(dayString[i]);
    }
    day.innerHTML = dayString[i].charAt(0);
    days.appendChild(day);
  }

  calDiv.appendChild(days);

  for(let i = 0; i < 24; i++){
    let hourRow = document.createElement('div');
    hourRow.classList.add('row');
    let timeColumn = createTimeColumn(i);
    hourRow.appendChild(timeColumn);

    for(let j = 1; j < 8; j++){

      let dayHour = document.createElement('div');
      dayHour.classList.add('col');
      dayHour.classList.add('inner');
      dayHour.classList.add(dayString[j]);
      //dayHour.innerHTML = dayString[j] + " " + hour + ":" + minutes;
      //dayHour.id =  dayString[j] + i;
      hourRow.appendChild(dayHour);

      let backgroundDiv = document.createElement('div');
      backgroundDiv.classList.add('background-div');
      backgroundDiv.classList.add('styled-box');
      backgroundDiv.id =  dayString[j] + i;
      dayHour.append(backgroundDiv);
    }
    calDiv.appendChild(hourRow);
  }
}

function createTimeColumn(hour){
  let div = document.createElement('div');
  div.classList.add('col');
  div.classList.add('time');
  let marker;
  if(hour < 12){
    marker  = 'am'
  }else{
    marker  = 'pm'
  }
  let innerTimeLong = document.createElement('p');
  let innerTimeShort = document.createElement('p');

  innerTimeLong.classList.add('time-long');
  innerTimeShort.classList.add('time-short');


  div.classList.add('text-muted');
  if(hour % 12 == 0){
    innerTimeLong.innerHTML = "12:00 " + marker;
    innerTimeShort.innerHTML = "12";
  }else{
    innerTimeLong.innerHTML = (hour % 12)+ ":00 " + marker;
    innerTimeShort.innerHTML = (hour % 12);
  }
  div.appendChild(innerTimeLong);
  div.appendChild(innerTimeShort);

  return div;
}

function resetCalendar(){
  $('#cal .class-info').remove();
  $('.background-div').css('height', '0px');
  colorIndex = 0;
  for(let i = 0; i < colors.length; i++){
    $("#cal .selected-" + colors[i]).removeClass('selected-' + colors[i]);
  }

  let calendar = document.getElementById('cal');
  let rows = calendar.childNodes;
  for(let i = 0; i < rows.length; i++){
    let row = rows[i];
    $(row).show();
    row.classList.remove('selected-row');
  }
}

function showCalendar(){
  $("#cal-container").show();
  $("#calendar-controls").show();
}

function hideCalendar(){
  $("#cal-container").hide();
  $("#calendar-controls").hide();
}

function loadPrevCombo(){
  if(displayedClassNum - 1 >= 0){
    resetCalendar();
    displayedClassNum--;
    highlightClasses(currentClasses[displayedClassNum]);
    document.getElementById("currentCourseNum").innerHTML = displayedClassNum + 1;
  }
}

function loadNextCombo(){
  if(displayedClassNum + 1 < currentClasses.length){
    resetCalendar();
    displayedClassNum++;
    highlightClasses(currentClasses[displayedClassNum]);
    document.getElementById("currentCourseNum").innerHTML = displayedClassNum + 1;
  }
}

function resizeCalender(){
 let calendar = document.getElementById('cal');
 let rows = calendar.childNodes;
 for(let i = 1; i < /*rows.length*/9; i++){ // Start calendar at 8am (unless classes are earlier)
   let row = rows[i];
   if(! row.classList.contains('selected-row')){
     $(row).hide();
   }else{
     break;
   }
 }

 for(let i = rows.length - 1; i > 18; i--){ // end calendar at 5pm (unless classes are later)
   let row = rows[i];
   if(! row.classList.contains('selected-row')){
     $(row).hide();
   }else{
     break;
   }
 }


}

function highlightClasses(classes){
  for(let i = 0; i < classes.length; i++){
    let currentClass = classes[i];
    highlightMeetings(currentClass);
  }
  resizeCalender();
}

function highlightMeetings(currentClass){
  let meetings = currentClass.meetings;
  for(let i = 0; i < meetings.length; i++){
    let meeting = meetings[i];

    let beginH = meeting.beginH;
    let beginM = meeting.beginM;
    let endH = meeting.endH;
    let endM = meeting.endM;


    for(let j = 0; j < meeting.days.length; j++){
      let day = meeting.days[j];
      highlightRange(day, beginH, beginM, endH, endM, colors[colorIndex], currentClass);
    }
  }
  colorIndex = (colorIndex + 1) % colors.length;
}

function highlightRange(day, beginH, beginM, endH, endM, color, currentClass){
  let calendarDayHeight = parseInt($(".col").css('height'));
  let isFirst = true;
  let hour = beginH;
  while(hour < endH){
    let topVal = (beginM / 60) * calendarDayHeight;
    let height = calendarDayHeight - topVal;
    if(isFirst){
      highlightSlot(day + hour, topVal, height, color, currentClass, true);
      isFirst = false;
    }else{
      highlightSlot(day + hour, topVal, height, color, currentClass, false);
    }
    hour++;
    beginM = 0;
  }

  if(beginM != endM){
    //let topVal = 2 * beginM;
    let topVal = (beginM / 60) * calendarDayHeight;

    let height = calendarDayHeight - topVal - (((60 - endM) / 60) * calendarDayHeight);
    if(isFirst){
      highlightSlot(day + hour, topVal, height,color, currentClass, true);
      isFirst = false;
    }else{
      highlightSlot(day + hour, topVal, height, color, currentClass, false);
    }
  }

}

function highlightSlot(id, top, height,color, currentClass, showName){
  let row = document.getElementById(id).parentNode.parentNode;
  let classID = user.getCourseByName(currentClass.name).id;
  row.classList.add('selected-row');
  let slot = document.getElementById(id);
  slot.classList.add('selected-color-' + classID);
  slot.style.height = height + "px";
  slot.style.top = top + "px";
  if(showName){
    let className = currentClass.name;
    let sectionCode = currentClass.sectionCode;

    let infoHolder = document.createElement('div');
    infoHolder.classList.add('class-info');

    let classNameHeader = document.createElement('p');
    classNameHeader.classList.add('classname-p');
    classNameHeader.classList.add('class-info');
    $(classNameHeader).text(className);
    setTooltip(classNameHeader, sectionCode, "bottom");
    infoHolder.appendChild(classNameHeader);

    // TODO Remove
    let hr = document.createElement('hr');
    hr.classList.add('calendar-break');
    //infoHolder.appendChild(hr);

    // TODO Remove
    let sectionInfo = document.createElement('p');
    sectionInfo.classList.add('section-p');
    sectionInfo.classList.add('class-info');
    sectionInfo.classList.add('calendar-text-small');
    $(sectionInfo).text(sectionCode);
    //infoHolder.appendChild(sectionInfo);

    slot.appendChild(infoHolder);
  }
}

function showNoCalenderResults(){
  alert("No courses without overlapping class times");
}
