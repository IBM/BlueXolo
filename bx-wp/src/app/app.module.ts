// Angular libraries
import { BrowserModule } from '@angular/platform-browser';
import { NgModule, Injector } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

// Angular Material libraries
import {
  MatIconModule,
  MatCardModule,
  MatButtonModule,
  MatMenuModule,
  MatToolbarModule,
  MatTooltipModule,
  MatSidenavModule,
  MatListModule,
  MatTreeModule
} from '@angular/material';

// Components
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { FooterComponent } from './footer/footer.component';
import { LineComponent } from './line/line.component';
import { InformationComponent } from './information/information.component';
import { SliderComponent } from './slider/slider.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { environment } from '../environments/environment';
import { DocumentationComponent } from './documentation/documentation.component';
import { AppRoutingModule } from './app-routing.module';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    FooterComponent,
    LineComponent,
    InformationComponent,
    SliderComponent,
    DocumentationComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatIconModule,
    MatCardModule,
    MatButtonModule,
    MatMenuModule,
    MatToolbarModule,
    MatTooltipModule,
    MatSidenavModule,
    MatListModule,
    MatTreeModule,
    AppRoutingModule,
    ServiceWorkerModule.register('ngsw-worker.js', { enabled: environment.production })
  ],
  entryComponents: [],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
