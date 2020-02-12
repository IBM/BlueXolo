import { NgModule }                 from '@angular/core';
import { RouterModule, Routes }     from '@angular/router';

import { AppComponent } from './app.component';
import { DocumentationComponent } from './documentation/documentation.component';

const appRoutes: Routes = [
    { path: '', component: AppComponent },
    { path: 'documentation', component: DocumentationComponent}
];

@NgModule({
    imports: [
        RouterModule.forRoot(appRoutes) 
    ],
    exports: [
        RouterModule 
    ]
})
export class AppRoutingModule { }