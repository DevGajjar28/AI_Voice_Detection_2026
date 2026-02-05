# Technical Documentation: AI Voice Detection System

## 1. Core Technology: Spectrogram-based CNN
Our system treats voice detection not as an audio problem, but as a **Computer Vision** problem.

### The Pipeline
1.  **Input**: Base64 MP3/WAV Audio.
2.  **Preprocessing (The "Lens")**:
    *   We convert the raw audio waveform into a **Mel-Spectrogram**.
    *   **Mel-Spectrogram**: A visual heatmap representing sound (Time vs. Frequency).
    *   **Parameters**: 91 Mel bands, 150 time steps (approx 3 seconds).
3.  **Model (The "Brain")**:
    *   **Architecture**: Deep Convolutional Neural Network (CNN).
    *   **Why CNN?**: Just as CNNs detect edges/shapes in photos, our model detects **digital artifacts** in the spectrogram image.

## 2. Detection Techniques (The "Fingerprints")
The model looks for specific artifacts left by AI generation engines (Neural Vocoders like WaveNet, HiFi-GAN):

| Artifact Type | Human Voice | AI Generated Voice |
| :--- | :--- | :--- |
| **Spectral Cutoff** | Frequencies decay naturally up to 20kHz+. | Sharp "black bar" cutoff often seen >16kHz. |
| **Phase Coherence** | Natural, messy phase relationships. | Unnaturally perfect or "smeared" phase. |
| **Micro-Tremors** | Contains organic jitter (breath, vocal fold vibration). | Often has "flat" or mathematically perfect pitch curves. |
| **Silence** | Contains "Room Tone" (background air noise). | Often contains "Absolute Zero" digital silence. |

**Why this supports 5 Languages:**
These artifacts are caused by the *rendering engine*, not the language. A "robot" voice in Tamil has the same spectral cutoff as a "robot" voice in English.

## 3. Known Loop Holes (Limitations)
Honesty about limitations is crucial for technical judges.

1.  **Low Bitrate / Compression**:
    *   *The Issue*: Aggressive MP3 compression (e.g., < 64kbps) removes high frequencies.
    *   *Result*: The model might confuse a compressed Human voice for AI (False Positive) because the high-freq data is missing.
2.  **Background Noise**:
    *   *The Issue*: Heavy background noise (traffic, music) can "mask" the delicate AI artifacts.
    *   *Result*: An AI voice hidden under loud music might be classified as Human (False Negative).
3.  **Re-recording (The "Analog Hole")**:
    *   *The Issue*: Playing an AI voice on a speaker and recording it with a phone.
    *   *Result*: The speaker/mic adds "room tone" and "organic noise," potentially fooling the model into thinking it's real.

## 4. Mitigation Strategies (Future Work)
*   **Data Augmentation**: Train the model on "noisy" and "compressed" AI samples to make it robust against low-quality audio.
*   **Liveness Detection**: Analyze the "Room Impulse Response" to detect if audio was played through a speaker (to close the "Analog Hole").
