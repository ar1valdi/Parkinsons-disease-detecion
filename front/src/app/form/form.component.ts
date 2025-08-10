import { Component, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ModalService } from '../services/modal.service';
import { isPlatformBrowser } from '@angular/common';
import { NnProcessingService } from '../services/nn-processing.service';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './form.component.html',
  styleUrl: './form.component.scss'
})
export class FormComponent implements OnInit {
  analysisForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    protected modalService: ModalService,
    @Inject(PLATFORM_ID) private platformId: Object,
    private nnProcessingService: NnProcessingService
  ) {}

  /**
   * Component initialization - sets up form and loads neural network model.
   */
  async ngOnInit(): Promise<void> {
    this.scrollToTop();
    
    this.analysisForm = this.fb.group({
      Age: ['', [Validators.required, Validators.min(18), Validators.max(120)]],
      Gender: ['', Validators.required],
      Ethnicity: ['', Validators.required],
      EducationLevel: ['', Validators.required],
      BMI: ['', [Validators.required, Validators.min(10), Validators.max(60)]],
      Smoking: ['', Validators.required],
      AlcoholConsumption: ['', [Validators.required, Validators.min(0), Validators.max(50)]],
      PhysicalActivity: ['', [Validators.required, Validators.min(0), Validators.max(20)]],
      DietQuality: ['', [Validators.required, Validators.min(1), Validators.max(10)]],
      SleepQuality: ['', [Validators.required, Validators.min(1), Validators.max(10)]],
      FamilyHistoryParkinsons: ['', Validators.required],
      TraumaticBrainInjury: ['', Validators.required],
      Hypertension: ['', Validators.required],
      Diabetes: ['', Validators.required],
      Depression: ['', Validators.required],
      Stroke: ['', Validators.required],
      SystolicBP: ['', [Validators.required, Validators.min(70), Validators.max(200)]],
      DiastolicBP: ['', [Validators.required, Validators.min(40), Validators.max(130)]],
      CholesterolTotal: ['', [Validators.required, Validators.min(100), Validators.max(400)]],
      CholesterolLDL: ['', [Validators.required, Validators.min(50), Validators.max(300)]],
      CholesterolHDL: ['', [Validators.required, Validators.min(20), Validators.max(150)]],
      CholesterolTriglycerides: ['', [Validators.required, Validators.min(50), Validators.max(500)]],
      UPDRS: ['', [Validators.required, Validators.min(0), Validators.max(200)]],
      MoCA: ['', [Validators.required, Validators.min(0), Validators.max(30)]],
      FunctionalAssessment: ['', [Validators.required, Validators.min(0), Validators.max(10)]],
      Tremor: ['', Validators.required],
      Rigidity: ['', Validators.required],
      Bradykinesia: ['', Validators.required],
      PosturalInstability: ['', Validators.required],
      SpeechProblems: ['', Validators.required],
      SleepDisorders: ['', Validators.required],
      Constipation: ['', Validators.required]
    });

    this.showDisclaimerIfNeeded();
    await this.nnProcessingService.load();
  }

  private scrollToTop(): void {
    if (isPlatformBrowser(this.platformId)) {
      window.scrollTo({
        top: 0
      });
    }
  }

  /**
   * Shows disclaimer modal if not previously acknowledged in this session.
   */
  private showDisclaimerIfNeeded(): void {
    if (!isPlatformBrowser(this.platformId)) return;
    
    const disclaimerAcknowledged = sessionStorage.getItem('disclaimerAcknowledged');
    
    if (!disclaimerAcknowledged) {
      this.modalService.showDisclaimerModal();
      
      if (isPlatformBrowser(this.platformId)) {
        sessionStorage.setItem('disclaimerAcknowledged', 'true');
      }
    }
  }

  /**
   * Handles form submission and initiates analysis.
   */
  onSubmit(): void {
    if (this.analysisForm.valid) {
      const formData = this.analysisForm.value;
      this.performAnalysis(formData);
    } else {
      this.markFormGroupTouched();
    }
  }

  /**
   * Marks all form controls as touched to trigger validation display.
   */
  private markFormGroupTouched(): void {
    Object.keys(this.analysisForm.controls).forEach(key => {
      const control = this.analysisForm.get(key);
      control?.markAsTouched();
    });
  }

  /**
   * Converts form data to feature array in the correct order for model input.
   * @param formData Form data object
   * @returns Array of 32 numeric features
   */
  private convertFormDataToFeatureArray(formData: any): number[] {
    const featureOrder = [
      'Age', 'Gender', 'Ethnicity', 'EducationLevel', 'BMI', 'Smoking', 
      'AlcoholConsumption', 'PhysicalActivity', 'DietQuality', 'SleepQuality',
      'FamilyHistoryParkinsons', 'TraumaticBrainInjury', 'Hypertension', 
      'Diabetes', 'Depression', 'Stroke', 'SystolicBP', 'DiastolicBP',
      'CholesterolTotal', 'CholesterolLDL', 'CholesterolHDL', 'CholesterolTriglycerides',
      'UPDRS', 'MoCA', 'FunctionalAssessment', 'Tremor', 'Rigidity', 
      'Bradykinesia', 'PosturalInstability', 'SpeechProblems', 'SleepDisorders', 'Constipation'
    ];

    const features: number[] = [];
    
    for (const fieldName of featureOrder) {
      let value = formData[fieldName];
      
      if (typeof value === 'string') {
        value = parseFloat(value);
      } else if (typeof value === 'boolean') {
        value = value ? 1 : 0;
      } else if (typeof value === 'number') {
        value = value;
      } else {
        value = 0;
      }
      
      if (isNaN(value)) {
        value = 0;
      }
      
      features.push(value);
    }
    
    if (features.length !== 32) {
      throw new Error(`Feature array length mismatch: expected 32, got ${features.length}`);
    }
    
    return features;
  }

  /**
   * Performs neural network analysis on form data and displays results.
   * @param data Form data to analyze
   */
  private performAnalysis(data: any): void {
    const featureArray = this.convertFormDataToFeatureArray(data);
    
    this.nnProcessingService.predict(featureArray).then(result => {
      this.modalService.showSuccessModal(
        `Wynik: ${result > 0.5 ? 'Pozytywny' : 'Negatywny'} z ${Math.abs(result - 0.5) * 200}% pewnością`,
        'Analiza Zakończona'
      );
    }).catch(() => {
      this.modalService.showErrorModal(
        'Wystąpił błąd podczas analizy. Spróbuj ponownie.',
        'Błąd Analizy'
      );
    });
  }

  /**
   * Checks if a form field has validation errors and should display error state.
   * @param fieldName Name of the form field
   * @returns True if field is invalid and touched/dirty
   */
  isFieldInvalid(fieldName: string): boolean {
    const field = this.analysisForm.get(fieldName);
    return field ? field.invalid && (field.dirty || field.touched) : false;
  }

  /**
   * Gets the error message for a form field.
   * @param fieldName Name of the form field
   * @returns Error message string or empty string if no error
   */
  getFieldError(fieldName: string): string {
    const field = this.analysisForm.get(fieldName);
    if (field && field.errors) {
      if (field.errors['required']) return 'To pole jest wymagane';
      if (field.errors['min']) return `Minimalna wartość to ${field.errors['min'].min}`;
      if (field.errors['max']) return `Maksymalna wartość to ${field.errors['max'].max}`;
    }
    return '';
  }
}
