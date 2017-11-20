class User{
  constructor(){
    this.courses = [];
  }

  getCourseByName(name){
    for(let i = 0; i < this.courses.length ; i++){
      if(this.courses[i].name.toLowerCase() == name.toLowerCase()){
        return this.courses[i];
      }
    }
    return null;
  }
}

class Course{
  constructor(name, sections){
    if(name != null){
      this.name = name;
    }else{
      this.name = "";
    }
    if(sections != null){
      this.sections = sections;
    }else{
      this.sections = [];
    }
  }

  getSectionByProfessor(professor){
    for(let i = 0; i < this.sections.length; i++){
      if(this.sections[i].professor.toLowerCase() == professor.toLowerCase()){
        return this.sections[i];
      }
    }
    return null;
  }
}
