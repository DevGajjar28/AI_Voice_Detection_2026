import soundfile as sf
import numpy as np

# Generate a 3-second 440Hz sine wave (simulating audio)
sr = 22050
t = np.linspace(0, 3, int(sr * 3))
y = 0.5 * np.sin(2 * np.pi * 440 * t)

sf.write('d:\\Hackathon\\HCL-Voice-Detector\\dummy_test_audio.wav', y, sr)
print("Created dummy_test_audio.wav")
