import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-top-menu',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './top-menu.component.html',
  styleUrl: './top-menu.component.scss'
})
export class TopMenuComponent {
  
  scrollToSection(sectionId: string) {
    const element = document.getElementById(sectionId);
    if (element) {
      // Account for fixed header height (80px)
      const headerHeight = 80;
      const elementPosition = element.offsetTop - headerHeight;
      
      window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
      });
    }
  }
}
