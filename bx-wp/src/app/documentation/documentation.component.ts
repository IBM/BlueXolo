import { Component, OnInit } from '@angular/core';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {NestedTreeControl} from '@angular/cdk/tree';
import { Router } from "@angular/router";
import { DomSanitizer } from '@angular/platform-browser';
import {
    transition,
    trigger,
    state,
    style,
    animate,
    group,
    animateChild
  } from '@angular/animations';

@Component({
  selector: 'app-documentation',
  templateUrl: './documentation.component.html',
  styleUrls: ['./documentation.component.css'],
  animations: [

    trigger(
      'enterAnimation', [
        state('enter', style({ transform: 'translateX(0)' })),
        transition(':enter', [
          style({transform: 'translateX(100%)', opacity: 0}),
          animate('500ms', style({transform: 'translateX(0)', opacity: 1}))
        ]),
        transition(':leave', [
          style({transform: 'translateX(0)', opacity: 1}),
          animate('500ms', style({transform: 'translateX(100%)', opacity: 0}))
        ])
      ]
    )



    ]
})
export class DocumentationComponent implements OnInit {
  showFiller = true;
  showToggleButton = false;
  currentState = 'enter';
  
  documentationItems = [
    {
      id: "0", 
      chapter: "BlueXolo Manual", 
      title: "BlueXolo Manual User", 
      content: "BlueXolo is a WEB framework that allows the generation of test scripts in a visual way using a “drag and drop” interface which allows the generation of complex test cases spending a minimum amount of time.", 
      img: ["assets/images/slides-overview/image1.png",
            "assets/images/slides-overview/image2.png",
            "assets/images/slides-overview/image3.png",
            "assets/images/slides-overview/image4.png"
          ]
    },
    {
      id: "1", 
      chapter: "First Steps", 
      title: "Requirements", 
      content: "",
      img: ["assets/images/documentation/first-steps/requirements/requirements-0.png"]
    },
    {
      id: "2", 
      chapter: "First Steps", 
      title: "Download", 
      content: "Go to our repository: ",
      link: "https://github.com/IBM/BlueXolo",
      img: ["assets/images/documentation/first-steps/download/download-0.png",
            "assets/images/documentation/first-steps/download/download-1.png"      
          ]
    },
    {
      id: "3", 
      chapter: "First Steps", 
      title: "Install", 
      content: "",
      img: ["assets/images/documentation/first-steps/install/install-0.png", 
            "assets/images/documentation/first-steps/install/install-1.png",
            "assets/images/documentation/first-steps/install/install-2.png",
            "assets/images/documentation/first-steps/install/install-3.png",
            "assets/images/documentation/first-steps/install/install-4.png",
            "assets/images/documentation/first-steps/install/install-5.png",
            "assets/images/documentation/first-steps/install/install-6.png",
            "assets/images/documentation/first-steps/install/install-7.png",
            "assets/images/documentation/first-steps/install/install-8.png",
            "assets/images/documentation/first-steps/install/install-9.png",
            "assets/images/documentation/first-steps/install/install-10.png",
            "assets/images/documentation/first-steps/install/install-11.png",
            "assets/images/documentation/first-steps/install/install-12.png"
          ] 
    },/*    
    {
      id: "4", 
      chapter: "Users", 
      title: "Users Management", 
      content: "", 
      video: this.sanitizer.bypassSecurityTrustResourceUrl("https://www.youtube-nocookie.com/embed/?showinfo=0&rel=0") 
    },
    {
      id: "5", 
      chapter: "Users", 
      title: "Create User", 
      content: "",
      video: this.sanitizer.bypassSecurityTrustResourceUrl("https://www.youtube-nocookie.com/embed/?showinfo=0&rel=0") 
    },*/
    {
      id: "4", 
      chapter: "Users", 
      title: "Request Access", 
      content: "Request Access", 
      img: ["assets/images/documentation/users/request-access/login-1.png", 
            "assets/images/documentation/users/request-access/login-2.png",
            "assets/images/documentation/users/request-access/login-3.png",
            "assets/images/documentation/users/request-access/login-4.png"
          ] 
    },
    {
      id: "5", 
      chapter: "Users", 
      title: "Forgotten Password", 
      content: "Get New Password", 
      img: ["assets/images/documentation/users/forgotten-password/login-1.png", 
            "assets/images/documentation/users/forgotten-password/login-5.png",
            "assets/images/documentation/users/forgotten-password/login-6.png"
          ]
    },
    {
      id: "6", 
      chapter: "Sources", 
      title: "Products", 
      content: "Create NewProduct", 
      img: ["assets/images/documentation/sources/products/product-1.png", 
            "assets/images/documentation/sources/products/product-2.png",
            "assets/images/documentation/sources/products/product-3.png",
            "assets/images/documentation/sources/products/product-4.png"
          ] 
    },
    {
      id: "7", 
      chapter: "Sources", 
      title: "Commands", 
      content: "Extract OS Commands", 
      img: ["assets/images/documentation/sources/commands/oscommands-0.png", 
            "assets/images/documentation/sources/commands/oscommands-1.png",
            "assets/images/documentation/sources/commands/oscommands-2.png",
            "assets/images/documentation/sources/commands/oscommands-3.png"
          ],
      video: this.sanitizer.bypassSecurityTrustResourceUrl("https://www.youtube-nocookie.com/embed/ReZXMvrFQOw?showinfo=0&rel=0")
    },
    {
      id: "8", 
      chapter: "Sources", 
      title: "Robot Framework", 
      content: "Add Robot Framework Version", 
      img: ["assets/images/documentation/sources/robot/robotversion-0.png", 
            "assets/images/documentation/sources/robot/robotversion-1.png",
            "assets/images/documentation/sources/robot/robotversion-2.png"
          ] 
    },
    {
      id: "9", 
      chapter: "Sources", 
      title: "Libraries", 
      content: "Add Libraries", 
      img: ["assets/images/documentation/sources/libraries/libraries-0.png", 
            "assets/images/documentation/sources/libraries/libraries-1.png",
            "assets/images/documentation/sources/libraries/libraries-2.png",
            "assets/images/documentation/sources/libraries/libraries-3.png"
          ],
          video: this.sanitizer.bypassSecurityTrustResourceUrl("https://www.youtube-nocookie.com/embed/ocdulq2vTL4?showinfo=0&rel=0")
    },
    {
      id: "10", 
      chapter: "Sources", 
      title: "Phases", 
      content: "Create New Phase", 
      img: ["assets/images/documentation/sources/phases/phases-0.png", 
            "assets/images/documentation/sources/phases/phases-1.png",
            "assets/images/documentation/sources/phases/phases-2.png",
            "assets/images/documentation/sources/phases/phases-3.png"
          ] 
    },
    {
      id: "11", 
      chapter: "Servers", 
      title: "Templates", 
      content: "Create New Template", 
      img: ["assets/images/documentation/servers/templates/template-0.png", 
            "assets/images/documentation/servers/templates/template-1.png",
            "assets/images/documentation/servers/templates/template-2.png",
            "assets/images/documentation/servers/templates/template-3.png",
          ] 
    },
    {
      id: "12", 
      chapter: "Servers", 
      title: "Profile", 
      content: "Create New Profile", 
      img: ["assets/images/documentation/servers/profile/profile-0.png", 
            "assets/images/documentation/servers/profile/profile-1.png",
            "assets/images/documentation/servers/profile/profile-2.png",
            "assets/images/documentation/servers/profile/profile-3.png"
          ] 
    },
    {
      id: "13", 
      chapter: "Servers", 
      title: "Parameters", 
      content: "Create New Parameter", 
      img: ["assets/images/documentation/servers/parameters/parameters-0.png", 
            "assets/images/documentation/servers/parameters/parameters-1.png",
            "assets/images/documentation/servers/parameters/parameters-2.png",
            "assets/images/documentation/servers/parameters/parameters-3.png",
          ] 
    },
    {
      id: "14", 
      chapter: "Contribute", 
      title: "GitHub Repository", 
      content: "Go to our repository: ",
      link: "https://github.com/IBM/BlueXolo",
      img: ["assets/images/documentation/contribute/github_repository/github_repository-1.png"]
    },
    {
      id: "15", 
      chapter: "Contribute", 
      title: "GitHub Forks", 
      content: "How to work with Forks on GitHub", 
      img: ["assets/images/documentation/contribute/github_fork/github_fork-1.png", 
            "assets/images/documentation/contribute/github_fork/github_fork-2.png",
            "assets/images/documentation/contribute/github_fork/github_fork-3.png",
            "assets/images/documentation/contribute/github_fork/github_fork-4.png",
            "assets/images/documentation/contribute/github_fork/github_fork-5.png",
            "assets/images/documentation/contribute/github_fork/github_fork-6.png",
            "assets/images/documentation/contribute/github_fork/github_fork-7.png",
            "assets/images/documentation/contribute/github_fork/github_fork-8.png",
            "assets/images/documentation/contribute/github_fork/github_fork-9.png",
            "assets/images/documentation/contribute/github_fork/github_fork-10.png",
            "assets/images/documentation/contribute/github_fork/github_fork-11.png",
            "assets/images/documentation/contribute/github_fork/github_fork-12.png",
            "assets/images/documentation/contribute/github_fork/github_fork-13.png",
            "assets/images/documentation/contribute/github_fork/github_fork-14.png"
          ] 
    },
  ];

  itemSelected = this.documentationItems[0];

  treeControl = new NestedTreeControl<FoodNode>(node => node.children);
  dataSource = new MatTreeNestedDataSource<FoodNode>();


  constructor(private router: Router, private sanitizer: DomSanitizer) {
    this.dataSource.data = TREE_DATA;
  }

  ngOnInit() {
  }

  hasChild = (_: number, node: FoodNode) => !!node.children && node.children.length > 0;

  changeItem(itemSelected) {
    let result = this.documentationItems.findIndex( item => item.title === itemSelected );
    if(result >= 0){
      this.itemSelected = this.documentationItems[result];
    }
  }

  changeItemArrows(buttonArrow) {

    let result = this.documentationItems.findIndex( item => item.title === this.itemSelected.title );
    
    if(result >= 0){
      if(buttonArrow === 'next') {
        ++result;
        if(result < this.documentationItems.length){
          this.itemSelected = this.documentationItems[result];
          this.changeState();
        }
      } else {
        if(result >= 1){
          --result;
          this.itemSelected = this.documentationItems[result];
          this.changeState();
        }
      }
    }
  }

  goHome() {
    this.router.navigate(['/']);
  }

  goDocumentation() {
    this.router.navigate(['/documentation']);
  }

  changeState() {
    this.currentState = this.currentState === 'enter' ? 'leave' : 'enter';
  }
}

interface FoodNode {
  name: string;
  children?: FoodNode[];
}

const TREE_DATA: FoodNode[] = [
  {
    name: 'First Steps',
    children: [
      {name: 'Requirements'},
      {name: 'Download'},
      {name: 'Install'}
    ]
  }, {
    name: 'Users',
    children: [
      /*{name: 'Users Management'},
      {name: 'Create User'},*/
      {name: 'Request Access'},
      {name: 'Forgotten Password'},
    ]
  }, {
    name: 'Sources',
    children: [
      {name: 'Products'},
      {name: 'Commands'},
      {name: 'Robot Framework'},
      {name: 'Libraries'},
      {name: 'Phases'},
    ]
  },  {
    name: 'Servers',
    children: [
      {name: 'Templates'},
      {name: 'Profile'},
      {name: 'Parameters'}
    ]
  },/* {
    name: 'Testing',
    children: [
      {name: 'Collections'},
      {
        name: 'Keywords',
        children: [
          {name: 'Create'},
          {name: 'Run'},
        ]
      }, {
        name: 'Test Cases',
        children: [
          {name: 'Create'},
          {name: 'Run'},
        ]
      },
      {
        name: 'Test Suites',
        children: [
          {name: 'Create'},
          {name: 'Run'},
        ]
      },
    ]
  },*/  {
    name: 'Contribute',
    children: [
      {name: 'GitHub Repository'},
      {name: 'GitHub Forks'}
    ]
  },
];