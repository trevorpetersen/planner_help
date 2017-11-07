"use strict"
var exports = module.exports = {};

class BasicClass{
  constructor(className, professor, sectionCode, meetings){
    if(className.indexOf(' ') != -1){
      let classParts = className.split(' ');
      className = classParts[0].substring(0,1).toUpperCase() + classParts[0].substring(1).toLowerCase() + ' ' +classParts[1];
    }else if(className.length > 0){
      className = className.substring(0,1).toUpperCase() + className.substring(1).toLowerCase();
    }

    this.name = className;
    this.professor = professor;
    this.sectionCode = sectionCode;
    if(meetings != null){
      this.meetings = meetings;
    }else{
      this.meetings = new Array();
    }
  }

  addMeeting(meeting){
    this.meetings.push(meeting);
  }
};

exports.Meeting = class Meeting{
  constructor(dayCode, beginH, beginM, endH, endM){
    this.dayCode = dayCode;
    this.beginH = beginH;
    this.beginM = beginM;
    this.endH = endH;
    this.endM = endM;
    this.days = new Array();
    this.time = this.getTime(dayCode + "", beginH, beginM, endH, endM);
  }

  getTime(dayCode, beginH, beginM, endH, endM){
    if(dayCode == null || parseInt(dayCode) == NaN){
      return [];
    }
    let times = new Array();
    for(let i = 0; i < dayCode.length; i++){
      let code = parseInt(dayCode.charAt(i));
      this.addDay(code);

      let start = this.getMinutes(code, beginH, beginM);
      let end = this.getMinutes(code, endH, endM);

      times.push([start, end]);
    }
    return times;
  }

  getMinutes(day, hour, min){
    const MINUTES_IN_DAY = 60 * 24;
    let mins = 0;
    let currentCode = parseInt(day);
    mins += (currentCode * MINUTES_IN_DAY);
    mins += ((60 * hour) + min);

    return mins;
  }

  addDay(code){
    switch(code){
      case 1:
        this.days.push('Mo')
        break;
      case 2:
        this.days.push('Tu')
        break;
      case 3:
        this.days.push('We')
        break;
      case 4:
        this.days.push('Th')
        break;
      case 5:
        this.days.push('Fr')
        break;
      case 6:
        this.days.push('Sa')
        break;
      case 7:
        this.days.push('Su')
        break;
    }
  }
}

exports.Course = class Course extends BasicClass{
  constructor(className, professor, sectionCode, meetings){
    super(className, professor, sectionCode, meetings);
    this.discussions = new Array();
  }

  addDiscussion(discussion){
    this.discussions.push(discussion);
  }
};

exports.Discussion = class Discussion extends BasicClass{
  constructor(className, professor, sectionCode, meetings){
    super(className, sectionCode, meetings);
  }
};
