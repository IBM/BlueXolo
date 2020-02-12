import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-information',
  templateUrl: './information.component.html',
  styleUrls: ['./information.component.css']
})
export class InformationComponent implements OnInit {

  items = [
    {
      name: 'Main Characteristics',
      link: 'https://github.com/IBM/BlueXolo/blob/master/Main_Characteristics.md', 
      icon: 'fa fa-code fa-5x'
    },{
      name: 'Installation Guide', 
      link: 'https://github.com/IBM/BlueXolo/blob/master/INSTALL.md',
      icon: 'fa fa-laptop fa-5x'
    },
    {
      name: 'How To Contribute', 
      link:'https://github.com/IBM/BlueXolo/blob/master/How_To_Contribute.md', 
      icon: 'fa fa-github fa-5x'
    }
  ];


  constructor() { }

  ngOnInit() {
  }

}
