import { Component } from '@angular/core';
import { HeroComponent } from '../hero/hero.component';
import { FloatingIconsComponent } from '../floating-icons/floating-icons.component';
import { AboutProjectComponent } from '../about-project/about-project.component';
import { NeuralNetworkComponent } from '../neural-network/neural-network.component';

@Component({
  selector: 'app-landing-page',
  imports: [HeroComponent, AboutProjectComponent, NeuralNetworkComponent],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.scss'
})
export class LandingPageComponent {
}
