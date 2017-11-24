var customColors = ["#e74c3c", "#FFEB3B", "#2980b9", "#9b59b6", "#e67e22", "#34495e", "#1abc9c"];

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

  getColorByID(id){
    for(let i = 0; i < this.courses.length ; i++){
      if(this.courses[i].id == id){
        return customColors[i];
      }
    }
    return "#ffffff";
  }

}

class Course{
  constructor(name, sections, id){
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

    this.id = id;
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
