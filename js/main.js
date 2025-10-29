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
        // System generation selector
        document.getElementById('systemGeneration').addEventListener('change', (e) => {
            this.handleGenerationChange(e.target.value);
        });
        
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

        // Help modal
        document.getElementById('showHelp').addEventListener('click', () => {
            document.getElementById('helpModal').classList.remove('hidden');
        });
        document.querySelector('.close-modal').addEventListener('click', () => {
            document.getElementById('helpModal').classList.add('hidden');
        });
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('helpModal');
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });

        // Initialize with text input visible
        this.handleSourceTypeChange('text');
        this.handleGenerationChange('5g');
    }

    handleGenerationChange(generation) {
        const infoText = document.getElementById('generationInfo');
        const sourceCodec = document.getElementById('sourceCodec');
        const channelCodec = document.getElementById('channelCodec');
        
        // Update description and available options based on generation
        if (generation === '5g') {
            infoText.textContent = '5G: LDPC/Polar para canal, hasta 256-QAM';
            // Enable standard codecs
            Array.from(sourceCodec.options).forEach(opt => {
                if (opt.value === 'learned') opt.disabled = true;
                else opt.disabled = false;
            });
        } else if (generation === '5g-advanced') {
            infoText.textContent = '5G Avanzado: Mejoras en MIMO, eficiencia espectral';
            Array.from(sourceCodec.options).forEach(opt => {
                if (opt.value === 'learned') opt.disabled = true;
            });
        } else if (generation === '6g') {
            infoText.textContent = '6G: Codificación conjunta (JSCC/DeepJSCC)';
            // Enable learned codec for 6G
            Array.from(sourceCodec.options).forEach(opt => {
                opt.disabled = false;
            });
        }
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
            const decodedChannel = await this.decodeChannel(llrs, encodedChannel);

            // Step 8: Source decoding
            await this.updateProgress(90, 'Decodificando fuente...');
            const reconstructed = await this.decodeSource(decodedChannel, sourceData);

            // Step 9: Calculate metrics
            await this.updateProgress(95, 'Calculando métricas...');
            await this.calculateMetrics(sourceData, reconstructed, encodedSource.bits, decodedChannel);

            // Step 10: Update all visualizations
            await this.updateProgress(100, 'Completado');
            await this.updateAllVisualizations(sourceData, reconstructed);

            // Re-enable button
            runButton.disabled = false;
            document.getElementById('runButtonText').textContent = 'Ejecutar Simulación';
            
            // Hide progress bar after a delay
            setTimeout(() => {
                document.getElementById('progressBar').classList.add('hidden');
            }, 1000);

        } catch (error) {
            console.error('Error en la simulación:', error);
            
            // Show user-friendly error message
            const errorMsg = document.createElement('div');
            errorMsg.style.cssText = 'background: #fee; border: 2px solid #c00; padding: 1rem; margin: 1rem; border-radius: 0.5rem;';
            errorMsg.innerHTML = `
                <strong style="color: #c00;">❌ Error en la simulación</strong>
                <p style="margin: 0.5rem 0;">${error.message}</p>
                <p style="font-size: 0.85rem; color: #666;">Revise la consola del navegador (F12) para más detalles.</p>
            `;
            document.getElementById('inputDisplay').prepend(errorMsg);
            
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
            generation: document.getElementById('systemGeneration').value,
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
        const codec = this.config.sourceCodec;
        
        // Display input
        if (data.type === 'text') {
            Visualizer.displayText(data.original, 'inputDisplay');
        }
        
        if (codec === 'none') {
            // Just convert to binary bits array
            const bits = data.binary.split('').map(b => parseInt(b));
            Visualizer.displayBinary(data.binary, 'sourceEncodedDisplay', 400);
            return { bits, originalLength: data.length, encodedLength: data.length };
        } else if (codec === 'huffman') {
            // Apply Huffman coding
            const huffman = new HuffmanCoder();
            const encoded = huffman.encode(data.binary);
            Visualizer.displayBinary(encoded.encoded, 'sourceEncodedDisplay', 400);
            return { 
                bits: encoded.encoded.split('').map(b => parseInt(b)),
                huffmanTree: encoded.tree,
                originalLength: data.length,
                encodedLength: encoded.encoded.length
            };
        }
        
        // Default: no encoding
        const bits = data.binary.split('').map(b => parseInt(b));
        Visualizer.displayBinary(data.binary, 'sourceEncodedDisplay', 400);
        return { bits, originalLength: data.length, encodedLength: data.length };
    }

    async encodeChannel(data) {
        const codec = this.config.channelCodec;
        const bits = data.bits;
        
        if (codec === 'none') {
            const display = document.getElementById('channelEncodedDisplay');
            display.innerHTML = `<p class="info-text">Sin codificación de canal</p>
                <p class="info-text">${bits.length} bits</p>`;
            return { bits, codeRate: 1.0 };
        } else if (codec === 'ldpc') {
            const coder = new LDPCCoder(this.config.codeRate, 648);
            const encoded = coder.encode(bits);
            const display = document.getElementById('channelEncodedDisplay');
            display.innerHTML = `<p class="info-text">LDPC (tasa ${this.config.codeRate})</p>
                <p class="info-text">${encoded.length} bits codificados</p>
                <pre class="bits-display">${encoded.slice(0, 200).join('').match(/.{1,8}/g).join(' ')}...</pre>`;
            return { bits: encoded, codeRate: this.config.codeRate, decoder: coder };
        } else if (codec === 'polar') {
            const k = Math.floor(bits.length * this.config.codeRate);
            const n = Math.pow(2, Math.ceil(Math.log2(bits.length / this.config.codeRate)));
            const coder = new PolarCoder(n, k);
            const encoded = coder.encode(bits);
            const display = document.getElementById('channelEncodedDisplay');
            display.innerHTML = `<p class="info-text">Polar (tasa ${this.config.codeRate})</p>
                <p class="info-text">${encoded.length} bits codificados</p>
                <pre class="bits-display">${encoded.slice(0, 200).join('').match(/.{1,8}/g).join(' ')}...</pre>`;
            return { bits: encoded, codeRate: this.config.codeRate, decoder: coder };
        }
        
        return { bits, codeRate: 1.0 };
    }

    async modulate(data) {
        const scheme = this.config.modulation;
        const symbols = Modulator.modulate(data.bits, scheme);
        
        // Visualize constellation
        Visualizer.plotConstellation(symbols, 'constellationPreChannel', 'Señal Modulada (Pre-Canal)');
        
        return { symbols, scheme, bitsPerSymbol: Modulator.getBitsPerSymbol(scheme) };
    }

    async applyChannel(signal) {
        const snrDB = this.config.channelValue;
        const channelResult = AWGNChannel.addNoise(
            signal.symbols, 
            snrDB, 
            signal.bitsPerSymbol,
            1.0
        );
        
        // Visualize received signal with ideal points
        Visualizer.plotConstellationWithIdeal(
            channelResult.symbols,
            signal.symbols,
            'constellationPostChannel',
            `Señal Recibida (SNR = ${snrDB} dB)`
        );
        
        return { 
            symbols: channelResult.symbols, 
            original: signal.symbols,
            noiseVariance: channelResult.noiseVariance 
        };
    }

    async demodulate(received, modulationData) {
        const scheme = modulationData.scheme;
        const llrs = Demodulator.demodulateSoft(
            received.symbols,
            scheme,
            received.noiseVariance
        );
        
        // Visualize LLRs
        if (llrs.length > 0) {
            Visualizer.plotLLRHistogram(llrs, 'llrHistogram');
        }
        
        const display = document.getElementById('decodedDisplay');
        display.innerHTML = `<p class="info-text">${llrs.length} LLRs calculados</p>
            <p class="info-text">Rango: [${Math.min(...llrs).toFixed(2)}, ${Math.max(...llrs).toFixed(2)}]</p>`;
        
        return { llrs, scheme };
    }

    async decodeChannel(llrs, channelData) {
        if (!channelData.decoder) {
            // Hard decision on LLRs
            const bits = llrs.llrs.map(llr => llr < 0 ? 1 : 0);
            return bits;
        }
        
        return channelData.decoder.decode(llrs.llrs);
    }

    async decodeSource(data, sourceData) {
        // For now, just convert bits back to text if it's text
        if (this.config.sourceType === 'text') {
            const bytes = [];
            for (let i = 0; i < data.length; i += 8) {
                const byte = data.slice(i, i + 8);
                const byteStr = byte.join('');
                bytes.push(parseInt(byteStr.padEnd(8, '0'), 2));
            }
            
            const decoder = new TextDecoder();
            const text = decoder.decode(new Uint8Array(bytes));
            return { type: 'text', text };
        }
        
        return data;
    }

    async calculateMetrics(sourceData, reconstructed, transmittedBits, receivedBits) {
        // Calculate BER
        let bitErrors = 0;
        const minLength = Math.min(transmittedBits.length, receivedBits.length);
        
        for (let i = 0; i < minLength; i++) {
            if (transmittedBits[i] !== receivedBits[i]) {
                bitErrors++;
            }
        }
        
        const ber = minLength > 0 ? bitErrors / minLength : 0;
        
        // Calculate SER - handle potential null return
        let ser = Metrics.calculateSER(transmittedBits, receivedBits, 
            Modulator.getBitsPerSymbol(this.config.modulation));
        
        // If SER calculation failed (null), calculate it manually
        if (ser === null) {
            const bitsPerSymbol = Modulator.getBitsPerSymbol(this.config.modulation);
            let symbolErrors = 0;
            for (let i = 0; i < minLength; i += bitsPerSymbol) {
                let symbolError = false;
                for (let j = 0; j < bitsPerSymbol && i + j < minLength; j++) {
                    if (transmittedBits[i + j] !== receivedBits[i + j]) {
                        symbolError = true;
                        break;
                    }
                }
                if (symbolError) symbolErrors++;
            }
            const numSymbols = Math.ceil(minLength / bitsPerSymbol);
            ser = numSymbols > 0 ? symbolErrors / numSymbols : 0;
        }
        
        this.results.metrics = {
            ber,
            ser,
            bitErrors,
            totalBits: minLength
        };
        
        // Calculate information theory metrics
        const bitsArray = sourceData.binary.split('').map(b => parseInt(b));
        const entropyX = InformationTheory.calculateEntropy(bitsArray);
        const entropyY = InformationTheory.calculateEntropy(receivedBits);
        const mutualInfo = InformationTheory.calculateMutualInformation(
            bitsArray.slice(0, minLength), 
            receivedBits.slice(0, minLength)
        );
        
        this.results.infoTheory = {
            entropyX,
            entropyY,
            mutualInfo,
            capacity: InformationTheory.channelCapacityDB(this.config.channelValue)
        };
        
        // Text comparison
        if (sourceData.type === 'text' && reconstructed.type === 'text') {
            this.results.textComparison = {
                original: sourceData.original,
                reconstructed: reconstructed.text,
                levenshtein: Metrics.levenshteinDistance(sourceData.original, reconstructed.text)
            };
        }
    }

    async updateAllVisualizations(sourceData, reconstructed) {
        // Update output display
        if (reconstructed && reconstructed.type === 'text') {
            const outputDisplay = document.getElementById('outputDisplay');
            outputDisplay.innerHTML = `
                <h4>Texto Reconstruido:</h4>
                <pre style="white-space: pre-wrap; word-wrap: break-word;">${reconstructed.text}</pre>
            `;
        }
        
        // Update comparison
        if (this.results.textComparison) {
            const compDisplay = document.getElementById('comparisonDisplay');
            compDisplay.innerHTML = `
                <div style="margin-bottom: 1rem;">
                    <h4>Original:</h4>
                    <pre style="white-space: pre-wrap; word-wrap: break-word; font-size: 0.85rem;">${this.results.textComparison.original}</pre>
                </div>
                <div>
                    <h4>Reconstruido:</h4>
                    <pre style="white-space: pre-wrap; word-wrap: break-word; font-size: 0.85rem;">${this.results.textComparison.reconstructed}</pre>
                </div>
                <p class="info-text">Distancia de Levenshtein: ${this.results.textComparison.levenshtein}</p>
            `;
        }
        
        // Update system stats
        const statsBody = document.getElementById('systemStatsBody');
        statsBody.innerHTML = `
            <tr><td>SNR configurado</td><td class="metric-value">${this.config.channelValue} dB</td></tr>
            <tr><td>Modulación</td><td class="metric-value">${this.config.modulation.toUpperCase()}</td></tr>
            <tr><td>Código de canal</td><td class="metric-value">${this.config.channelCodec === 'none' ? 'Ninguno' : this.config.channelCodec.toUpperCase()}</td></tr>
            <tr><td>Tasa de código</td><td class="metric-value">${this.config.codeRate}</td></tr>
        `;
        
        // Update metrics display
        this.displayMetrics();
        this.displayInfoTheory();
    }

    displayMetrics() {
        const tbody = document.getElementById('metricsTableBody');
        
        // Check if metrics exist and have valid values
        if (!this.results || !this.results.metrics || 
            this.results.metrics.ber === null || this.results.metrics.ber === undefined ||
            this.results.metrics.ser === null || this.results.metrics.ser === undefined) {
            tbody.innerHTML = `<tr><td colspan="2">Esperando simulación...</td></tr>`;
            return;
        }
        
        const m = this.results.metrics;
        
        // Color code BER
        let berClass = 'metric-good';
        if (m.ber > 0.01) berClass = 'metric-bad';
        else if (m.ber > 0.001) berClass = 'metric-warning';
        
        tbody.innerHTML = `
            <tr><td>BER (Bit Error Rate)</td><td class="metric-value ${berClass}">${m.ber.toExponential(2)}</td></tr>
            <tr><td>SER (Symbol Error Rate)</td><td class="metric-value">${m.ser.toExponential(2)}</td></tr>
            <tr><td>Errores de bits</td><td class="metric-value">${m.bitErrors} / ${m.totalBits}</td></tr>
        `;
    }

    displayInfoTheory() {
        const tbody = document.getElementById('infoTheoryTableBody');
        
        // Check if info theory results exist and have valid values
        if (!this.results || !this.results.infoTheory ||
            this.results.infoTheory.entropyX === null || this.results.infoTheory.entropyX === undefined ||
            this.results.infoTheory.entropyY === null || this.results.infoTheory.entropyY === undefined ||
            this.results.infoTheory.mutualInfo === null || this.results.infoTheory.mutualInfo === undefined ||
            this.results.infoTheory.capacity === null || this.results.infoTheory.capacity === undefined) {
            tbody.innerHTML = `<tr><td colspan="2">Esperando simulación...</td></tr>`;
            return;
        }
        
        const it = this.results.infoTheory;
        tbody.innerHTML = `
            <tr><td>H(X) Entropía Entrada</td><td class="metric-value">${it.entropyX.toFixed(3)} bits/símbolo</td></tr>
            <tr><td>H(Y) Entropía Salida</td><td class="metric-value">${it.entropyY.toFixed(3)} bits/símbolo</td></tr>
            <tr><td>I(X;Y) Info. Mutua</td><td class="metric-value">${it.mutualInfo.toFixed(3)} bits/símbolo</td></tr>
            <tr><td>C Capacidad (Shannon)</td><td class="metric-value">${it.capacity.toFixed(3)} bits/canal</td></tr>
        `;
    }
}

// Initialize simulator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.simulator = new Simulator();
});

export default Simulator;
