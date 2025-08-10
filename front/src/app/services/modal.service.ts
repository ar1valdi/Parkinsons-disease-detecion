import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface ModalConfig {
  id: string;
  title?: string;
  message: string;
  buttonText?: string;
  type?: 'warning' | 'info' | 'error' | 'success';
  icon?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ModalService {
  private modalSubject = new BehaviorSubject<ModalConfig | null>(null);
  public modal$ = this.modalSubject.asObservable();

  showModal(config: ModalConfig): void {
    this.modalSubject.next(config);
  }

  hideModal(): void {
    this.modalSubject.next(null);
  }

  // Convenience methods for common modals
  showDisclaimerModal(): void {
    this.showModal({
      id: 'disclaimer',
      message: 'System First Sign nie gwarantuje poprawności wyników. Algorytm analizujący dane stworzony został jedynie w celach edukacyjnych i nie powinien służyć jako diagnoza medyczna.',
      buttonText: 'Rozumiem',
      type: 'warning',
      icon: 'warning'
    });
  }

  showSuccessModal(message: string, title?: string): void {
    this.showModal({
      id: 'success',
      title,
      message,
      buttonText: 'OK',
      type: 'success',
      icon: 'success'
    });
  }

  showErrorModal(message: string, title?: string): void {
    this.showModal({
      id: 'error',
      title: title || 'Błąd',
      message,
      buttonText: 'Zamknij',
      type: 'error',
      icon: 'error'
    });
  }
}
