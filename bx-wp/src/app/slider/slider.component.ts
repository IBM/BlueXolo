import { Component, OnInit } from '@angular/core';
import { Slide } from './slide'; 
import { SliderService } from '../slider.service';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent implements OnInit {

  sliderArray: object[];
  transform: number;
  selectedIndex: number = 0;

  constructor(private sliderService: SliderService) { 
    this.sliderArray = [];
    this.selectedIndex = 0;
    this.transform = 100;
  }

  ngOnInit() {
    this.sliderService.getDataSlides().subscribe(
      (slide: Slide) => this.sliderArray = slide.sliderArray
    );
  }

  selected(x) {
    this.downSelected(x);
    this.selectedIndex = x;
  }

  keySelected(x) {
    this.downSelected(x);
    this.selectedIndex = x;
  }

  downSelected(x) {
    this.transform = 100 - (x) * 45;
    this.selectedIndex = this.selectedIndex + 1;
    if(this.selectedIndex > 5) {
      this.selectedIndex = 0;
    }
  }

}
