# Sample Data Files

This directory contains sample data files for testing the communication simulator.

## Files

### Text (`text/sample_text.txt`)
- Simple text file for text transmission examples
- Contains Lorem Ipsum placeholder text
- Used to test Huffman and Arithmetic encoding

### Image (`image/sample_image.npy`)
- 64x64 grayscale test image (NumPy array)
- Contains gradient and circular patterns
- Stored as uint8 values (0-255)
- Load with: `image = np.load('data/image/sample_image.npy')`

### Audio (`audio/sample_audio.npy`)
- 1 second audio signal at 16 kHz sampling rate
- Musical note A4 (440 Hz) with harmonics
- Stored as int16 PCM values
- Load with: `audio = np.load('data/audio/sample_audio.npy')`

### Video (`video/sample_video.npy`)
- 30 frames of 32x32 grayscale video
- Moving sine wave pattern
- Stored as uint8 values (0-255)
- Shape: (num_frames, height, width)
- Load with: `video = np.load('data/video/sample_video.npy')`

## Usage

```python
import numpy as np

# Load image
image = np.load('data/image/sample_image.npy')
print(f"Image shape: {image.shape}")

# Load audio
audio = np.load('data/audio/sample_audio.npy')
print(f"Audio samples: {len(audio)}")

# Load video
video = np.load('data/video/sample_video.npy')
print(f"Video shape: {video.shape}")  # (frames, height, width)
```

## Generating New Data

To regenerate sample data, run:

```bash
python generate_sample_data.py
```

This will create new synthetic test files with default parameters.

## Notes

- All files are stored as NumPy arrays (.npy format) for simplicity
- Image and video use uint8 (0-255 range)
- Audio uses int16 PCM format (-32768 to 32767)
- These are synthetic data for testing - not real-world data

## Real Data

For testing with real data:
- **Images**: Use datasets like Kodak, USC-SIPI, or your own images
- **Audio**: Use TIMIT, LibriSpeech, or other speech datasets
- **Video**: Use standard test sequences (Foreman, Akiyo, etc.)

Convert real data to NumPy format and place in appropriate directories.
