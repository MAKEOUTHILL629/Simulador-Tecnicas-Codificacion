// Source Data Generators

export class SourceGenerator {
    /**
     * Convert text string to binary representation
     */
    static async generateText(text) {
        const encoder = new TextEncoder();
        const bytes = encoder.encode(text);
        
        // Convert to binary string
        const binary = Array.from(bytes)
            .map(byte => byte.toString(2).padStart(8, '0'))
            .join('');
        
        return {
            type: 'text',
            original: text,
            binary: binary,
            bytes: bytes,
            length: binary.length
        };
    }

    /**
     * Process image data to extractable format
     */
    static async generateImage(imageData) {
        const { width, height, data } = imageData;
        
        // Extract RGB channels (ignoring alpha)
        const pixels = [];
        for (let i = 0; i < data.length; i += 4) {
            pixels.push({
                r: data[i],
                g: data[i + 1],
                b: data[i + 2]
            });
        }
        
        // Convert to binary
        const binary = pixels.map(p => 
            p.r.toString(2).padStart(8, '0') +
            p.g.toString(2).padStart(8, '0') +
            p.b.toString(2).padStart(8, '0')
        ).join('');
        
        return {
            type: 'image',
            width: width,
            height: height,
            pixels: pixels,
            binary: binary,
            length: binary.length
        };
    }

    /**
     * Process audio samples
     */
    static async generateAudio(samples, sampleRate = 44100) {
        // Convert float samples to 16-bit PCM
        const pcm = new Int16Array(samples.length);
        for (let i = 0; i < samples.length; i++) {
            // Clamp to [-1, 1] and scale to 16-bit
            const s = Math.max(-1, Math.min(1, samples[i]));
            pcm[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
        }
        
        // Convert to binary
        const binary = Array.from(pcm)
            .map(sample => {
                // Handle negative numbers correctly
                const unsigned = sample < 0 ? 0x10000 + sample : sample;
                return unsigned.toString(2).padStart(16, '0');
            })
            .join('');
        
        return {
            type: 'audio',
            samples: samples,
            pcm: pcm,
            sampleRate: sampleRate,
            binary: binary,
            length: binary.length,
            duration: samples.length / sampleRate
        };
    }

    /**
     * Process video frames
     */
    static async generateVideo(frames) {
        // Process each frame as an image
        const processedFrames = [];
        let totalBinary = '';
        
        for (const frame of frames) {
            const frameData = await this.generateImage(frame);
            processedFrames.push(frameData);
            totalBinary += frameData.binary;
        }
        
        return {
            type: 'video',
            frames: processedFrames,
            frameCount: frames.length,
            width: processedFrames[0].width,
            height: processedFrames[0].height,
            binary: totalBinary,
            length: totalBinary.length
        };
    }

    /**
     * Convert binary string to byte array
     */
    static binaryToBytes(binary) {
        const bytes = [];
        for (let i = 0; i < binary.length; i += 8) {
            const byte = binary.slice(i, i + 8).padEnd(8, '0');
            bytes.push(parseInt(byte, 2));
        }
        return new Uint8Array(bytes);
    }

    /**
     * Convert byte array to binary string
     */
    static bytesToBinary(bytes) {
        return Array.from(bytes)
            .map(byte => byte.toString(2).padStart(8, '0'))
            .join('');
    }
}
