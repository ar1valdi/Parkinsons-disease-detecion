import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { ModalService, ModalConfig } from '../../services/modal.service';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './modal.component.html',
  styleUrl: './modal.component.scss'
})
export class ModalComponent implements OnInit, OnDestroy {
  modalConfig: ModalConfig | null = null;
  isVisible = false;
  private subscription: Subscription = new Subscription();

  constructor(private modalService: ModalService) {}

  ngOnInit(): void {
    this.subscription = this.modalService.modal$.subscribe(config => {
      this.modalConfig = config;
      this.isVisible = !!config;
    });
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  onClose(): void {
    this.modalService.hideModal();
  }

  onButtonClick(): void {
    this.modalService.hideModal();
  }

  getIconClass(): string {
    if (!this.modalConfig?.icon) return '';
    
    switch (this.modalConfig.icon) {
      case 'warning': return 'warning-icon';
      case 'error': return 'error-icon';
      case 'info': return 'info-icon';
      case 'success': return 'success-icon';
      default: return '';
    }
  }

  getModalClass(): string {
    if (!this.modalConfig?.type) return 'modal-default';
    
    switch (this.modalConfig.type) {
      case 'warning': return 'modal-warning';
      case 'error': return 'modal-error';
      case 'info': return 'modal-info';
      case 'success': return 'modal-success';
      default: return 'modal-default';
    }
  }
}
