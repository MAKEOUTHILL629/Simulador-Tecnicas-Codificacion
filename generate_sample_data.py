#!/usr/bin/env python3
"""
Script to generate sample data files for testing the simulator.

This script creates synthetic test data for:
- Images (grayscale test pattern)
- Audio (sine wave signal)
- Video (simulated as sequence of images)
"""

import numpy as np
import os


def generate_sample_image(output_path='data/image/sample_image.npy', size=(64, 64)):
    """
    Generate a simple grayscale test image with patterns.
    
    Args:
        output_path: Where to save the image
        size: Image dimensions (height, width)
    
    Returns:
        Image array
    """
    height, width = size
    
    # Create a gradient pattern
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    X, Y = np.meshgrid(x, y)
    
    # Combination of patterns: gradient + circles
    image = 0.5 * X + 0.3 * Y
    
    # Add circular pattern
    center_x, center_y = width // 2, height // 2
    for i in range(height):
        for j in range(width):
            dist = np.sqrt((i - center_y)**2 + (j - center_x)**2)
            if dist < width // 4:
                image[i, j] += 0.3 * np.sin(dist * 0.5)
    
    # Normalize to 0-255
    image = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
    
    # Save as numpy array
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.save(output_path, image)
    
    print(f"✓ Sample image generated: {output_path}")
    print(f"  Shape: {image.shape}, Range: [{image.min()}, {image.max()}]")
    
    return image


def generate_sample_audio(output_path='data/audio/sample_audio.npy', 
                         duration=1.0, sample_rate=16000):
    """
    Generate a simple audio signal (combination of sine waves).
    
    Args:
        output_path: Where to save the audio
        duration: Duration in seconds
        sample_rate: Sampling rate in Hz
    
    Returns:
        Audio array
    """
    # Generate time vector
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create a musical note (combination of frequencies)
    # A4 note (440 Hz) with harmonics
    fundamental = 440  # Hz
    audio = (0.5 * np.sin(2 * np.pi * fundamental * t) +
             0.25 * np.sin(2 * np.pi * 2 * fundamental * t) +
             0.125 * np.sin(2 * np.pi * 3 * fundamental * t))
    
    # Add envelope (fade in/out)
    envelope = np.ones_like(audio)
    fade_samples = int(0.05 * sample_rate)  # 50ms fade
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    audio = audio * envelope
    
    # Normalize to [-1, 1]
    audio = audio / np.max(np.abs(audio))
    
    # Convert to 16-bit PCM range
    audio_int16 = (audio * 32767).astype(np.int16)
    
    # Save as numpy array
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.save(output_path, audio_int16)
    
    print(f"✓ Sample audio generated: {output_path}")
    print(f"  Duration: {duration}s, Sample rate: {sample_rate}Hz")
    print(f"  Samples: {len(audio_int16)}, Range: [{audio_int16.min()}, {audio_int16.max()}]")
    
    return audio_int16


def generate_sample_video(output_path='data/video/sample_video.npy',
                         num_frames=30, frame_size=(32, 32)):
    """
    Generate a simple video (moving pattern).
    
    Args:
        output_path: Where to save the video
        num_frames: Number of frames
        frame_size: Frame dimensions (height, width)
    
    Returns:
        Video array
    """
    height, width = frame_size
    frames = []
    
    for frame_idx in range(num_frames):
        # Create moving pattern
        x = np.linspace(0, 2*np.pi, width)
        y = np.linspace(0, 2*np.pi, height)
        X, Y = np.meshgrid(x, y)
        
        # Moving sine wave pattern
        phase = 2 * np.pi * frame_idx / num_frames
        frame = np.sin(X + phase) * np.cos(Y + phase * 0.5)
        
        # Normalize to 0-255
        frame = ((frame - frame.min()) / (frame.max() - frame.min()) * 255).astype(np.uint8)
        frames.append(frame)
    
    video = np.array(frames)
    
    # Save as numpy array
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.save(output_path, video)
    
    print(f"✓ Sample video generated: {output_path}")
    print(f"  Frames: {num_frames}, Frame size: {frame_size}")
    print(f"  Shape: {video.shape}, Range: [{video.min()}, {video.max()}]")
    
    return video


def create_readme(data_dir='data'):
    """Create a README explaining the data files."""
    readme_content = """# Sample Data Files

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
"""
    
    readme_path = os.path.join(data_dir, 'README.md')
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✓ README generated: {readme_path}")


def main():
    """Generate all sample data files."""
    print("="*70)
    print("Generating Sample Data Files")
    print("="*70)
    print()
    
    # Generate image
    generate_sample_image()
    print()
    
    # Generate audio
    generate_sample_audio()
    print()
    
    # Generate video
    generate_sample_video()
    print()
    
    # Create README
    create_readme()
    print()
    
    print("="*70)
    print("✓ All sample data files generated successfully!")
    print("="*70)
    print()
    print("Data files location:")
    print("  - data/image/sample_image.npy")
    print("  - data/audio/sample_audio.npy")
    print("  - data/video/sample_video.npy")
    print("  - data/README.md")
    print()
    print("You can now run the examples in main.py to use these files.")


if __name__ == "__main__":
    main()
