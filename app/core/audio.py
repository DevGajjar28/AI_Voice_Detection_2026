import base64
import io
import librosa
import numpy as np
import tempfile
import os

def decode_base64_audio(base64_string):
    """
    Decodes a Base64 string into bytes.
    """
    try:
        return base64.b64decode(base64_string)
    except Exception as e:
        raise ValueError(f"Invalid Base64 string: {str(e)}")

def load_audio_from_bytes(audio_bytes, sr=22050):
    """
    Loads audio bytes (MP3/WAV/etc) into a librosa-compatible numpy array.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(audio_bytes)
        temp_path = temp_file.name

    try:
        # Load with librosa (it supports MP3 if ffmpeg is installed)
        # We use a try-except block to handle format issues
        y, sample_rate = librosa.load(temp_path, sr=sr)
        return y, sample_rate
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

def preprocess_audio(y, sr, n_mels=91, max_time_steps=150):
    """
    Converts audio time-series into Mel-spectrogram chunks expected by the model.
    Returns a numpy array of shape (N_chunks, n_mels, max_time_steps).
    """
    # Calculate hop_length to match the time steps roughly
    # The original repo didn't specify hop_length, so it used default 512.
    # 150 time steps * 512 samples/step / 22050 Hz ~= 3.4 seconds.
    
    # We will split the audio into chunks of this size
    chunk_length_samples = max_time_steps * 512
    
    # If audio is shorter than one chunk, pad it
    if len(y) < chunk_length_samples:
        y = np.pad(y, (0, chunk_length_samples - len(y)), mode='constant')
    
    # Split into chunks with 50% overlap
    chunks = []
    step = chunk_length_samples // 2
    
    for start in range(0, len(y) - chunk_length_samples + 1, step):
        end = start + chunk_length_samples
        chunk = y[start:end]
        
        # Compute Mel Spectrogram
        mel_spec = librosa.feature.melspectrogram(y=chunk, sr=sr, n_mels=n_mels)
        mel_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Ensure exact shape (n_mels, max_time_steps)
        if mel_db.shape[1] > max_time_steps:
            mel_db = mel_db[:, :max_time_steps]
        elif mel_db.shape[1] < max_time_steps:
            mel_db = np.pad(mel_db, ((0, 0), (0, max_time_steps - mel_db.shape[1])), mode='constant')
            
        chunks.append(mel_db)
        
    if not chunks:
        # Handle case where audio was just slightly longer than 0 but shorter than step
        # (Already handled by initial padding, but safe fallback)
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
        mel_db = librosa.power_to_db(mel_spec, ref=np.max)
        if mel_db.shape[1] < max_time_steps:
            mel_db = np.pad(mel_db, ((0, 0), (0, max_time_steps - mel_db.shape[1])), mode='constant')
        else:
             mel_db = mel_db[:, :max_time_steps]
        chunks.append(mel_db)

    return np.array(chunks)
