# Data Strategy & Hackathon Execution Plan

## 1. Goal
Support voice detection for **Tamil, English, Hindi, Malayalam, Telugu** with >95% accuracy, using minimal computing resources.

## 2. The Challenge
The current pre-trained model is likely trained on English/Western datasets. It may misclassify Indian languages as "AI" due to different tonal patterns or recording environments, or fail to detect AI in those languages.

## 3. Strategy: "Validate, Then Fine-tune"

### Phase 1: Rapid Validation (Do this first!)
Don't assume the model fails. Test it.
1. **Collect Samples**:
   - **Human**: Download 5-10 clips per language from [Mozilla Common Voice](https://commonvoice.mozilla.org/) (Tamil, Hindi, Malayalam, Telugu are available).
   - **AI**: Generate 5-10 clips per language using **ElevenLabs** (supports multilingual) or **Google TTS**.
2. **Run Tests**:
   - Use the API to test these samples.
   - Record Accuracy: `(Correct Predictions / Total Samples) * 100`.

### Phase 2: Data Collection (If Accuracy < 80%)
If the model struggles, you need a small "calibration" dataset.
- **Human Sources**:
  - YouTube Interviews (clean audio, high quality).
  - Mozilla Common Voice (filtered for high SNR).
- **AI Sources**:
  - Generate ~20 clips per language using:
    - **ElevenLabs** (Best for high-quality deepfakes).
    - **Murf.ai** (Good for Indian accents).
    - **Narakeet** (Supports many Indian languages).

### Phase 3: Minimal Fine-Tuning (Transfer Learning)
**Crucial for Laptop Constraints**: Do NOT train from scratch.
1. **Technique**: Transfer Learning.
   - Freeze the "Feature Extractor" (CNN layers).
   - Only retrain the final "Classification Head" (Dense layers).
2. **Resources Needed**:
   - ~50-100 samples per language.
   - Training time: < 30 mins on CPU.
3. **Process**:
   - Load `model-1.keras`.
   - `model.trainable = False` (Freeze base).
   - Add new Dense layer.
   - Train on your small 5-language dataset.

## 4. Winning Edge: Explanation
We have implemented a logic-based explanation engine that provides reasons based on confidence scores:
- **High Confidence AI**: "Spectral discontinuities detected" (Technical term for vocoder artifacts).
- **High Confidence Human**: "Natural breath patterns and organic pitch fluctuations."

## 5. Next Steps for You
1. **Download 5 human/AI samples** for one Indian language (e.g., Hindi).
2. **Test** using the running API.
3. If it fails, we will write a script to "fine-tune" the model lightly.
