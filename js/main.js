// Main Simulator Orchestrator
import { SourceGenerator } from './source-generators.js';
import { HuffmanCoder, DCTCoder, MDCTCoder } from './source-coding.js';
import { LDPCCoder, PolarCoder } from './channel-coding.js';
import { Modulator, Demodulator } from './modulation.js';
import { AWGNChannel } from './channel.js';
import { Metrics } from './metrics.js';
import { Visualizer } from './visualization.js';
import { InformationTheory } from './info-theory.js';

class Simulator {
    constructor() {
        this.sourceData = null;
        this.config = {};
        this.results = {};
        this.initUI();
    }

    initUI() {
        // Source type selector
        document.getElementById('sourceType').addEventListener('change', (e) => {
            this.handleSourceTypeChange(e.target.value);
        });

        // Quality factor slider
        document.getElementById('qualityFactor').addEventListener('input', (e) => {
            document.getElementById('qualityValue').textContent = e.target.value;
        });

        // Source codec selector
        document.getElementById('sourceCodec').addEventListener('change', (e) => {
            this.handleSourceCodecChange(e.target.value);
        });

        // Channel codec selector
        document.getElementById('channelCodec').addEventListener('change', (e) => {
            this.handleChannelCodecChange(e.target.value);
        });

        // Run simulation button
        document.getElementById('runSimulation').addEventListener('click', () => {
            this.runSimulation();
        });

        // Sample text button
        document.getElementById('loadSampleText').addEventListener('click', () => {
            this.loadSampleText();
        });

        // Sample image buttons
        document.getElementById('loadLena').addEventListener('click', () => {
            this.loadSampleImage('lena');
        });
        document.getElementById('loadBaboon').addEventListener('click', () => {
            this.loadSampleImage('baboon');
        });

        // Sample audio button
        document.getElementById('loadSampleAudio').addEventListener('click', () => {
            this.loadSampleAudio();
        });

        // Generate synthetic video
        document.getElementById('generateSyntheticVideo').addEventListener('click', () => {
            this.generateSyntheticVideo();
        });

        // File inputs
        document.getElementById('imageFile').addEventListener('change', (e) => {
            this.handleImageUpload(e.target.files[0]);
        });
        document.getElementById('audioFile').addEventListener('change', (e) => {
            this.handleAudioUpload(e.target.files[0]);
        });

        // Initialize with text input visible
        this.handleSourceTypeChange('text');
    }

    handleSourceTypeChange(type) {
        // Hide all source inputs
        document.querySelectorAll('.source-input').forEach(el => el.classList.add('hidden'));
        
        // Show selected source input
        const inputMap = {
            'text': 'textInput',
            'image': 'imageInput',
            'audio': 'audioInput',
            'video': 'videoInput'
        };
        document.getElementById(inputMap[type]).classList.remove('hidden');

        // Update source codec options availability
        this.updateSourceCodecOptions(type);
    }

    updateSourceCodecOptions(sourceType) {
        const codecSelect = document.getElementById('sourceCodec');
        const options = codecSelect.options;
        
        // Enable/disable options based on source type
        for (let i = 0; i < options.length; i++) {
            const value = options[i].value;
            if (value === 'dct' && (sourceType === 'image' || sourceType === 'video')) {
                options[i].disabled = false;
            } else if (value === 'mdct' && sourceType === 'audio') {
                options[i].disabled = false;
            } else if (value === 'dct' || value === 'mdct') {
                options[i].disabled = true;
            }
        }
    }

    handleSourceCodecChange(codec) {
        const dctQuality = document.getElementById('dctQuality');
        if (codec === 'dct') {
            dctQuality.classList.remove('hidden');
        } else {
            dctQuality.classList.add('hidden');
        }
    }

    handleChannelCodecChange(codec) {
        const codeRateParam = document.getElementById('codeRateParam');
        if (codec === 'none') {
            codeRateParam.classList.add('hidden');
        } else {
            codeRateParam.classList.remove('hidden');
        }
    }

    loadSampleText() {
        const sampleText = "La teoría de la información, desarrollada por Claude Shannon en 1948, establece los fundamentos matemáticos de la comunicación digital. El teorema de separación demuestra que la codificación de fuente y canal pueden optimizarse independientemente para alcanzar la capacidad del canal.";
        document.getElementById('textArea').value = sampleText;
    }

    async loadSampleImage(name) {
        // For now, create a simple colored pattern
        // In production, would load actual sample images
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');
        
        if (name === 'lena') {
            // Create a gradient pattern
            const gradient = ctx.createLinearGradient(0, 0, 256, 256);
            gradient.addColorStop(0, '#ff6b6b');
            gradient.addColorStop(1, '#4ecdc4');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, 256, 256);
        } else if (name === 'baboon') {
            // Create a more complex pattern
            for (let i = 0; i < 256; i += 16) {
                for (let j = 0; j < 256; j += 16) {
                    ctx.fillStyle = `hsl(${(i + j) % 360}, 70%, 50%)`;
                    ctx.fillRect(i, j, 16, 16);
                }
            }
        }
        
        this.sourceData = ctx.getImageData(0, 0, 256, 256);
        this.displayInputPreview(canvas);
    }

    async loadSampleAudio() {
        // Generate a simple sine wave for demonstration
        const sampleRate = 44100;
        const duration = 2; // seconds
        const frequency = 440; // Hz (A4 note)
        const samples = new Float32Array(sampleRate * duration);
        
        for (let i = 0; i < samples.length; i++) {
            samples[i] = Math.sin(2 * Math.PI * frequency * i / sampleRate);
        }
        
        this.sourceData = samples;
        this.displayAudioWaveform(samples, sampleRate);
    }

    async generateSyntheticVideo() {
        // Generate 10 frames of a moving square
        const frames = [];
        const width = 128;
        const height = 128;
        
        for (let f = 0; f < 10; f++) {
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            
            // Background
            ctx.fillStyle = '#2c3e50';
            ctx.fillRect(0, 0, width, height);
            
            // Moving square
            const x = (width / 11) * (f + 1) - 10;
            const y = height / 2 - 10;
            ctx.fillStyle = '#e74c3c';
            ctx.fillRect(x, y, 20, 20);
            
            frames.push(ctx.getImageData(0, 0, width, height));
        }
        
        this.sourceData = frames;
        this.displayVideoPreview(frames);
    }

    async handleImageUpload(file) {
        if (!file) return;
        
        const img = new Image();
        img.onload = () => {
            const canvas = document.createElement('canvas');
            canvas.width = Math.min(img.width, 512);
            canvas.height = Math.min(img.height, 512);
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            
            this.sourceData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            this.displayInputPreview(canvas);
        };
        img.src = URL.createObjectURL(file);
    }

    async handleAudioUpload(file) {
        if (!file) return;
        
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const arrayBuffer = await file.arrayBuffer();
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
        
        this.sourceData = audioBuffer.getChannelData(0); // Get first channel
        this.displayAudioWaveform(this.sourceData, audioBuffer.sampleRate);
    }

    displayInputPreview(canvas) {
        const display = document.getElementById('inputDisplay');
        display.innerHTML = '';
        display.appendChild(canvas);
    }

    displayAudioWaveform(samples, sampleRate) {
        const display = document.getElementById('inputDisplay');
        display.innerHTML = '<div id="audioWaveform"></div>';
        
        // Downsample for visualization
        const step = Math.max(1, Math.floor(samples.length / 1000));
        const waveform = [];
        const time = [];
        
        for (let i = 0; i < samples.length; i += step) {
            time.push(i / sampleRate);
            waveform.push(samples[i]);
        }
        
        Visualizer.plotWaveform(time, waveform, 'audioWaveform');
    }

    displayVideoPreview(frames) {
        const display = document.getElementById('inputDisplay');
        const canvas = document.createElement('canvas');
        canvas.width = frames[0].width;
        canvas.height = frames[0].height;
        const ctx = canvas.getContext('2d');
        ctx.putImageData(frames[0], 0, 0);
        
        display.innerHTML = '';
        display.appendChild(canvas);
        const info = document.createElement('p');
        info.className = 'info-text';
        info.textContent = `${frames.length} fotogramas, ${frames[0].width}×${frames[0].height}`;
        display.appendChild(info);
    }

    async runSimulation() {
        try {
            // Disable button and show progress
            const runButton = document.getElementById('runSimulation');
            runButton.disabled = true;
            document.getElementById('runButtonText').textContent = 'Procesando...';
            document.getElementById('progressBar').classList.remove('hidden');

            // Collect configuration
            this.config = this.getConfiguration();

            // Step 1: Get source data
            await this.updateProgress(10, 'Preparando fuente...');
            const sourceData = await this.prepareSourceData();

            // Step 2: Source encoding
            await this.updateProgress(20, 'Codificando fuente...');
            const encodedSource = await this.encodeSource(sourceData);

            // Step 3: Channel encoding
            await this.updateProgress(35, 'Codificando canal...');
            const encodedChannel = await this.encodeChannel(encodedSource);

            // Step 4: Modulation
            await this.updateProgress(50, 'Modulando señal...');
            const modulatedSignal = await this.modulate(encodedChannel);

            // Step 5: Channel (add noise)
            await this.updateProgress(60, 'Aplicando ruido del canal...');
            const receivedSignal = await this.applyChannel(modulatedSignal);

            // Step 6: Demodulation
            await this.updateProgress(70, 'Demodulando señal...');
            const llrs = await this.demodulate(receivedSignal, modulatedSignal);

            // Step 7: Channel decoding
            await this.updateProgress(80, 'Decodificando canal...');
            const decodedChannel = await this.decodeChannel(llrs);

            // Step 8: Source decoding
            await this.updateProgress(90, 'Decodificando fuente...');
            const reconstructed = await this.decodeSource(decodedChannel);

            // Step 9: Calculate metrics
            await this.updateProgress(95, 'Calculando métricas...');
            await this.calculateMetrics(sourceData, reconstructed, encodedSource, llrs);

            // Step 10: Update all visualizations
            await this.updateProgress(100, 'Completado');
            await this.updateAllVisualizations();

            // Re-enable button
            runButton.disabled = false;
            document.getElementById('runButtonText').textContent = 'Ejecutar Simulación';
            
            // Hide progress bar after a delay
            setTimeout(() => {
                document.getElementById('progressBar').classList.add('hidden');
            }, 1000);

        } catch (error) {
            console.error('Error en la simulación:', error);
            alert('Error durante la simulación: ' + error.message);
            
            const runButton = document.getElementById('runSimulation');
            runButton.disabled = false;
            document.getElementById('runButtonText').textContent = 'Ejecutar Simulación';
            document.getElementById('progressBar').classList.add('hidden');
        }
    }

    async updateProgress(percent, message) {
        document.getElementById('progressFill').style.width = percent + '%';
        // Allow UI to update
        await new Promise(resolve => setTimeout(resolve, 10));
    }

    getConfiguration() {
        return {
            sourceType: document.getElementById('sourceType').value,
            sourceCodec: document.getElementById('sourceCodec').value,
            qualityFactor: parseInt(document.getElementById('qualityFactor').value),
            channelCodec: document.getElementById('channelCodec').value,
            codeRate: parseFloat(document.getElementById('codeRate').value),
            modulation: document.getElementById('modulation').value,
            channelMetric: document.getElementById('channelMetric').value,
            channelValue: parseFloat(document.getElementById('channelValue').value)
        };
    }

    async prepareSourceData() {
        const sourceType = this.config.sourceType;
        
        if (sourceType === 'text') {
            const text = document.getElementById('textArea').value;
            if (!text) throw new Error('Por favor ingrese texto');
            return await SourceGenerator.generateText(text);
        } else if (this.sourceData) {
            return this.sourceData;
        } else {
            throw new Error('Por favor cargue o genere datos de fuente');
        }
    }

    async encodeSource(data) {
        // For now, return simple binary representation
        // Full implementation would use the selected codec
        return { data: data, encoded: true };
    }

    async encodeChannel(data) {
        // Placeholder for channel encoding
        return data;
    }

    async modulate(data) {
        // Placeholder for modulation
        return [];
    }

    async applyChannel(signal) {
        // Placeholder for channel noise
        return signal;
    }

    async demodulate(received, original) {
        // Placeholder for demodulation
        return [];
    }

    async decodeChannel(llrs) {
        // Placeholder for channel decoding
        return null;
    }

    async decodeSource(data) {
        // Placeholder for source decoding
        return data;
    }

    async calculateMetrics(original, reconstructed, encoded, llrs) {
        this.results.metrics = {
            ber: 0,
            ser: 0,
            psnr: 0,
            ssim: 0
        };
        this.results.infoTheory = {
            entropyX: 0,
            entropyY: 0,
            mutualInfo: 0
        };
    }

    async updateAllVisualizations() {
        // Update metrics display
        this.displayMetrics();
        this.displayInfoTheory();
    }

    displayMetrics() {
        const tbody = document.getElementById('metricsTableBody');
        tbody.innerHTML = `
            <tr><td>BER (Bit Error Rate)</td><td class="metric-value">${this.results.metrics.ber.toExponential(2)}</td></tr>
            <tr><td>SER (Symbol Error Rate)</td><td class="metric-value">${this.results.metrics.ser.toExponential(2)}</td></tr>
            <tr><td>PSNR (dB)</td><td class="metric-value">${this.results.metrics.psnr.toFixed(2)}</td></tr>
            <tr><td>SSIM</td><td class="metric-value">${this.results.metrics.ssim.toFixed(4)}</td></tr>
        `;
    }

    displayInfoTheory() {
        const tbody = document.getElementById('infoTheoryTableBody');
        tbody.innerHTML = `
            <tr><td>H(X) Entropía Entrada</td><td class="metric-value">${this.results.infoTheory.entropyX.toFixed(3)} bits</td></tr>
            <tr><td>H(Y) Entropía Salida</td><td class="metric-value">${this.results.infoTheory.entropyY.toFixed(3)} bits</td></tr>
            <tr><td>I(X;Y) Info. Mutua</td><td class="metric-value">${this.results.infoTheory.mutualInfo.toFixed(3)} bits</td></tr>
        `;
    }
}

// Initialize simulator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.simulator = new Simulator();
});

export default Simulator;
