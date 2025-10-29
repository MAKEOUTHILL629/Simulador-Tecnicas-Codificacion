// Modulation and Demodulation

/**
 * Modulator - Maps bits to complex symbols
 */
export class Modulator {
    /**
     * Get constellation points for modulation scheme
     */
    static getConstellation(scheme) {
        switch (scheme) {
            case 'qpsk':
                return this.qpskConstellation();
            case '16qam':
                return this.qam16Constellation();
            case '64qam':
                return this.qam64Constellation();
            case '256qam':
                return this.qam256Constellation();
            default:
                return this.qpskConstellation();
        }
    }

    /**
     * QPSK constellation (Gray coded)
     */
    static qpskConstellation() {
        const scale = 1 / Math.sqrt(2);
        return [
            { real: scale, imag: scale },      // 00
            { real: scale, imag: -scale },     // 01
            { real: -scale, imag: scale },     // 10
            { real: -scale, imag: -scale }     // 11
        ];
    }

    /**
     * 16-QAM constellation (Gray coded)
     */
    static qam16Constellation() {
        const scale = 1 / Math.sqrt(10);
        const levels = [-3, -1, 1, 3];
        const constellation = [];

        for (let i = 0; i < 4; i++) {
            for (let q = 0; q < 4; q++) {
                constellation.push({
                    real: levels[q] * scale,
                    imag: levels[i] * scale
                });
            }
        }

        return constellation;
    }

    /**
     * 64-QAM constellation (Gray coded)
     */
    static qam64Constellation() {
        const scale = 1 / Math.sqrt(42);
        const levels = [-7, -5, -3, -1, 1, 3, 5, 7];
        const constellation = [];

        for (let i = 0; i < 8; i++) {
            for (let q = 0; q < 8; q++) {
                constellation.push({
                    real: levels[q] * scale,
                    imag: levels[i] * scale
                });
            }
        }

        return constellation;
    }

    /**
     * 256-QAM constellation (Gray coded)
     */
    static qam256Constellation() {
        const scale = 1 / Math.sqrt(170);
        const levels = [-15, -13, -11, -9, -7, -5, -3, -1, 1, 3, 5, 7, 9, 11, 13, 15];
        const constellation = [];

        for (let i = 0; i < 16; i++) {
            for (let q = 0; q < 16; q++) {
                constellation.push({
                    real: levels[q] * scale,
                    imag: levels[i] * scale
                });
            }
        }

        return constellation;
    }

    /**
     * Modulate bits to symbols
     */
    static modulate(bits, scheme) {
        const constellation = this.getConstellation(scheme);
        const bitsPerSymbol = Math.log2(constellation.length);
        const symbols = [];

        for (let i = 0; i < bits.length; i += bitsPerSymbol) {
            // Extract bits for this symbol
            const symbolBits = bits.slice(i, i + bitsPerSymbol);
            
            // Pad if necessary
            while (symbolBits.length < bitsPerSymbol) {
                symbolBits.push(0);
            }

            // Convert bits to symbol index
            const index = symbolBits.reduce((acc, bit, idx) => 
                acc + bit * Math.pow(2, bitsPerSymbol - 1 - idx), 0);

            symbols.push(constellation[index]);
        }

        return symbols;
    }

    /**
     * Get bits per symbol for modulation scheme
     */
    static getBitsPerSymbol(scheme) {
        const constellations = {
            'qpsk': 2,
            '16qam': 4,
            '64qam': 6,
            '256qam': 8
        };
        return constellations[scheme] || 2;
    }
}

/**
 * Demodulator - Maps received symbols to bits/LLRs
 */
export class Demodulator {
    /**
     * Hard decision demodulation (minimum distance)
     */
    static demodulateHard(receivedSymbols, scheme) {
        const constellation = Modulator.getConstellation(scheme);
        const bitsPerSymbol = Math.log2(constellation.length);
        const bits = [];

        for (const received of receivedSymbols) {
            // Find nearest constellation point
            let minDist = Infinity;
            let nearestIndex = 0;

            for (let i = 0; i < constellation.length; i++) {
                const dist = this.euclideanDistance(received, constellation[i]);
                if (dist < minDist) {
                    minDist = dist;
                    nearestIndex = i;
                }
            }

            // Convert index to bits
            for (let b = bitsPerSymbol - 1; b >= 0; b--) {
                bits.push((nearestIndex >> b) & 1);
            }
        }

        return bits;
    }

    /**
     * Soft decision demodulation (LLR calculation)
     */
    static demodulateSoft(receivedSymbols, scheme, noiseVariance) {
        const constellation = Modulator.getConstellation(scheme);
        const bitsPerSymbol = Math.log2(constellation.length);
        const llrs = [];

        for (const y of receivedSymbols) {
            // Calculate LLR for each bit in the symbol
            for (let bitIdx = 0; bitIdx < bitsPerSymbol; bitIdx++) {
                const llr = this.calculateBitLLR(y, constellation, bitIdx, noiseVariance);
                llrs.push(llr);
            }
        }

        return llrs;
    }

    /**
     * Calculate LLR for a single bit using max-log approximation
     */
    static calculateBitLLR(y, constellation, bitIdx, noiseVariance) {
        const bitsPerSymbol = Math.log2(constellation.length);
        let minDist0 = Infinity;
        let minDist1 = Infinity;

        // Find minimum distance for bit=0 and bit=1
        for (let i = 0; i < constellation.length; i++) {
            const bitValue = (i >> (bitsPerSymbol - 1 - bitIdx)) & 1;
            const dist = this.euclideanDistance(y, constellation[i]);

            if (bitValue === 0 && dist < minDist0) {
                minDist0 = dist;
            } else if (bitValue === 1 && dist < minDist1) {
                minDist1 = dist;
            }
        }

        // Max-log approximation of LLR
        const llr = (minDist1 - minDist0) / (2 * noiseVariance);

        return llr;
    }

    /**
     * Calculate Euclidean distance between two complex points
     */
    static euclideanDistance(p1, p2) {
        const dr = p1.real - p2.real;
        const di = p1.imag - p2.imag;
        return dr * dr + di * di;
    }
}
