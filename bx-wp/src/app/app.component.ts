import { Component } from '@angular/core';
import { Router } from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
  title = 'BlueXolo';
  color = '#546e7a';
  spa: Boolean = false;

  constructor(private router: Router){}

  goHome() {
    this.spa = false;
    window.location.replace('#home');
  }

  goInformation() {
    this.spa = false;
    window.location.replace('#information');
  }

  goFooter() {
      this.spa = false;
      window.location.replace('#footer');
  }

  goDocumentation() {
    this.spa = true;
    this.router.navigate(['/documentation']);
  }
}
