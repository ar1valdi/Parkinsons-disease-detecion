import { Component, OnInit, OnDestroy, HostListener, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Router, NavigationEnd } from '@angular/router';
import { filter, takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-floating-icons',
  templateUrl: './floating-icons.component.html',
  styleUrl: './floating-icons.component.scss'
})
export class FloatingIconsComponent implements OnInit, OnDestroy {
  private scrollListener: (() => void) | undefined;
  private destroy$ = new Subject<void>();
  position: string = 'fixed'; // Default position

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object,
    private router: Router
  ) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.setupParallaxEffect();
      this.setupRouteListener();
    }
  }

  ngOnDestroy() {
    if (isPlatformBrowser(this.platformId) && this.scrollListener) {
      window.removeEventListener('scroll', this.scrollListener);
    }
    this.destroy$.next();
    this.destroy$.complete();
  }

  private setupRouteListener() {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd),
      takeUntil(this.destroy$)
    ).subscribe((event: NavigationEnd) => {
      // Set position based on current route
      if (event.url === '/' || event.url === '') {
        this.position = 'fixed'; // Landing page
      } else if (event.url === '/form') {
        this.position = 'fixed'; // Form page
      } else {
        this.position = 'absolute'; // Default for other routes
      }
    });
  }

  @HostListener('window:scroll', ['$event'])
  onScroll() {
    if (isPlatformBrowser(this.platformId)) {
      this.updateParallaxEffect();
    }
  }

  private setupParallaxEffect() {
    if (isPlatformBrowser(this.platformId)) {
      this.scrollListener = () => this.updateParallaxEffect();
      window.addEventListener('scroll', this.scrollListener);
    }
  }

  private updateParallaxEffect() {
    if (!isPlatformBrowser(this.platformId)) return;
    
    const scrolled = window.pageYOffset;
    const parallaxSpeed = 0.3; // Icons move at 30% of scroll speed for slower effect
    
    const icons = document.querySelectorAll('.floating-icons-container');
    icons.forEach((icon: Element, index: number) => {
      const element = icon as HTMLElement;
      const yPos = -(scrolled * parallaxSpeed);
      // Keep the floating animation while adding parallax
      element.style.transform = `translateY(${yPos}px) translateZ(0)`;
    });
  }
}
