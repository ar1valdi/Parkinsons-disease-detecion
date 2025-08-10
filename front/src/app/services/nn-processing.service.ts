import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { InferenceSession, Tensor, env } from 'onnxruntime-web';

@Injectable({ providedIn: 'root' })
export class NnProcessingService {
  private session?: InferenceSession;
  private modelLoadingPromise?: Promise<InferenceSession>;

  private readonly FEATURE_MEANS = [69.6019002375, 0.4926365796, 0.6926365796, 1.3372921615, 27.2094927652, 0.2964370546, 10.0404130324, 5.0166744480, 4.9129007701, 6.9966388434, 0.1458432304, 0.1064133017, 0.1458432304, 0.1482185273, 0.2052256532, 0.0489311164, 133.7197149644, 90.2498812352, 226.8608397688, 126.1478578621, 59.6703515413, 222.9404998224, 101.4153182771, 15.0943135462, 4.9896941861, 0.4318289786, 0.2527315914, 0.2076009501, 0.1387173397, 0.2950118765, 0.2451306413, 0.2969121140];
  
  private readonly FEATURE_STDS = [11.5917570926, 0.4999457771, 1.0035887781, 0.8956274265, 7.2063865929, 0.4566860270, 5.6856630658, 2.8902322474, 2.8714325356, 1.7526485611, 0.3529489801, 0.3083658718, 0.3529489801, 0.3553164723, 0.4038664191, 0.2157240419, 26.4960592403, 17.0574349386, 43.5790514713, 43.3967242979, 23.3653679312, 101.8716155319, 56.5780044593, 8.6409606913, 2.9331797284, 0.4953309115, 0.4345783406, 0.4055894422, 0.3456513263, 0.4560480997, 0.4301646313, 0.4568974837];

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  /**
   * Standardizes input features using training data statistics.
   * @param features Array of 32 raw feature values
   * @returns Array of standardized feature values
   */
  private standardizeFeatures(features: number[]): number[] {
    if (features.length !== 32) {
      throw new Error(`Expected 32 features, got ${features.length}`);
    }

    return features.map((value, index) => {
      const mean = this.FEATURE_MEANS[index];
      const std = this.FEATURE_STDS[index];
      return (value - mean) / std;
    });
  }

  /**
   * Loads the ONNX model for inference.
   * @returns Promise that resolves when model is loaded
   */
  async load(): Promise<void> {
    if (!isPlatformBrowser(this.platformId)) return;
    if (this.session || this.modelLoadingPromise) return;

    env.wasm.wasmPaths = 'https://cdn.jsdelivr.net/npm/onnxruntime-web@1.22.0/dist/';

    this.modelLoadingPromise = InferenceSession.create('/model.onnx', {
      executionProviders: ['wasm'],
      graphOptimizationLevel: 'all'
    });
    this.session = await this.modelLoadingPromise;
  }

  /**
   * Performs Parkinson's disease prediction using the neural network model.
   * @param features32 Array of 32 feature values
   * @returns Promise that resolves to prediction probability (0-1)
   */
  async predict(features32: number[]): Promise<number> {
    if (!isPlatformBrowser(this.platformId)) throw new Error('Browser only');
    if (features32.length !== 32) throw new Error('Expected 32 features');

    if (!this.session) await this.load();
    if (!this.session) throw new Error('Session not loaded');

    const standardizedFeatures = this.standardizeFeatures(features32);

    const inputName = this.session.inputNames[0] ?? 'input';
    const outputName = this.session.outputNames[0] ?? 'output';

    const input = new Tensor('float32', Float32Array.from(standardizedFeatures), [1, 32]);
    const feeds: Record<string, Tensor> = { [inputName]: input };

    const results = await this.session.run(feeds);
    return Number(results[outputName].data[0]);
  }
}