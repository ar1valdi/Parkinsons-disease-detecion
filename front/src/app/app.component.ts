import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TopMenuComponent } from './top-menu/top-menu.component';
import { FloatingIconsComponent } from './floating-icons/floating-icons.component';
import { FooterComponent } from './footer/footer.component';
import { ModalComponent } from './components/modal/modal.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, TopMenuComponent, FloatingIconsComponent, FooterComponent, ModalComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'front';
}
