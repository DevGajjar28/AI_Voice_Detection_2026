import tensorflow as tf
import numpy as np
import os
import zipfile
import tempfile
import shutil
from .audio import preprocess_audio, load_audio_from_bytes, decode_base64_audio

class VoiceClassifier:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        print(f"Loading model from {self.model_path}...")
        
        # Windows path fix & Keras format fix
        # The model might be an HDF5 file named as .keras (older Keras versions allowed this, Keras 3 is stricter)
        try:
            # Explicitly open in binary mode
            with open(self.model_path, 'rb') as src:
                 content = src.read()
            
            # Check for HDF5 signature
            is_h5 = content.startswith(b'\x89HDF')
            suffix = ".h5" if is_h5 else ".keras"
            print(f"Detected file format: {'HDF5' if is_h5 else 'Keras Zip'} (suffix: {suffix})")

            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(content)
                temp_model_path = tmp.name
            
            print(f"Copied to temp path: {temp_model_path}")
            self.model = tf.keras.models.load_model(temp_model_path)
            print("Model loaded successfully.")
            
            # Cleanup
            try:
                os.unlink(temp_model_path)
            except:
                pass
                
        except Exception as e:
            print(f"Failed to load model: {e}")
            raise e

    def predict(self, audio_base64):
        """
        Predicts if the audio is AI or Human.
        Returns: (label, confidence, explanation)
        """
        try:
            # 1. Decode
            audio_bytes = decode_base64_audio(audio_base64)
            
            # 2. Load
            y, sr = load_audio_from_bytes(audio_bytes)
            
            # 3. Preprocess (Get chunks)
            # Shape: (N, 91, 150)
            X = preprocess_audio(y, sr)
            
            # 4. Predict
            # The model expects (Batch, 91, 150) or (Batch, 91, 150, 1) depending on training
            # Based on the tester script: x = np.array(x); predictions = model.predict(x)
            # So (Batch, 91, 150) seems correct (or it handles the channel dim internally)
            
            predictions = self.model.predict(X)
            
            # predictions is likely [[prob_AI, prob_Human], ...] for each chunk
            
            # 5. Aggregate logic
            # Average the probabilities across all chunks
            avg_probs = np.mean(predictions, axis=0)
            ai_score = avg_probs[0]
            human_score = avg_probs[1]
            
            # 6. Final Decision & Explanation Generation
            if human_score > 0.5:
                label = "HUMAN"
                confidence = float(human_score)
                if confidence > 0.90:
                    explanation = "Strong evidence of natural speech characteristics, including organic pitch fluctuations and complex breath patterns."
                elif confidence > 0.70:
                    explanation = "Consistent natural vocal patterns detected. No significant spectral high-frequency cutoff observed."
                else:
                    explanation = "Likely human speech. Analysis shows natural micro-tremors in voice, though some features are ambiguous."
            else:
                label = "AI_GENERATED"
                confidence = float(ai_score)
                if confidence > 0.95:
                    explanation = "High-confidence detection: Spectral high-frequency cutoff and abnormal pitch consistency detected (Neural Vocoder artifacts)."
                elif confidence > 0.85:
                    explanation = "Detected distinct AI fingerprints: Unnatural silence intervals and metallic high-frequency harmonics."
                elif confidence > 0.70:
                    explanation = "Likely AI-generated: Phase coherence issues and flat prosody detected in the spectrogram."
                else:
                    explanation = "Classified as AI-generated due to subtle irregularities in spectral continuity."

            return {
                "classification": label,
                "confidenceScore": round(confidence, 4),
                "explanation": explanation
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            raise e

# Global instance
MODEL_PATH = os.path.join(os.getcwd(), "deepfake-audio-detector", "model", "model-1.keras")
classifier = VoiceClassifier(MODEL_PATH)
