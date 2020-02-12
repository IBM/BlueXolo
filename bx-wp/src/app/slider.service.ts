import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

const PATH = './assets/data/data-slides.json';

@Injectable({
 providedIn: 'root'
})
export class SliderService {

 constructor(private http: HttpClient) {
 }

 getDataSlides() {
   return this.http.get(PATH);
 }

}
