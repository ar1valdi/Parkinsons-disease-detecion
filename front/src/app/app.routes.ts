import { Routes } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { FormComponent } from './form/form.component';

export const routes: Routes = [
  { path: '', component: LandingPageComponent },
  { path: 'form', component: FormComponent },
  { path: '**', redirectTo: '' }
];
