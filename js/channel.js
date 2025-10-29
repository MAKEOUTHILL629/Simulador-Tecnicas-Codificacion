// AWGN Channel Model

/**
 * Additive White Gaussian Noise Channel
 */
export class AWGNChannel {
    /**
     * Add AWGN to complex symbols
     */
    static addNoise(symbols, snrDB, bitsPerSymbol, codeRate) {
        const snr = Math.pow(10, snrDB / 10);
        const noiseVariance = 1 / (2 * snr);

        const noisySymbols = symbols.map(s => ({
            real: s.real + this.gaussianRandom() * Math.sqrt(noiseVariance),
            imag: s.imag + this.gaussianRandom() * Math.sqrt(noiseVariance)
        }));

        return {
            symbols: noisySymbols,
            noiseVariance: noiseVariance,
            snr: snr,
            snrDB: snrDB
        };
    }

    /**
     * Calculate noise variance from Eb/N0
     */
    static noiseVarianceFromEbN0(ebN0DB, bitsPerSymbol, codeRate) {
        const ebN0 = Math.pow(10, ebN0DB / 10);
        const snr = ebN0 * bitsPerSymbol * codeRate;
        return 1 / (2 * snr);
    }

    /**
     * Convert SNR to Eb/N0
     */
    static snrToEbN0(snrDB, bitsPerSymbol, codeRate) {
        const snr = Math.pow(10, snrDB / 10);
        const ebN0 = snr / (bitsPerSymbol * codeRate);
        return 10 * Math.log10(ebN0);
    }

    /**
     * Convert Eb/N0 to SNR
     */
    static ebN0ToSnr(ebN0DB, bitsPerSymbol, codeRate) {
        const ebN0 = Math.pow(10, ebN0DB / 10);
        const snr = ebN0 * bitsPerSymbol * codeRate;
        return 10 * Math.log10(snr);
    }

    /**
     * Generate Gaussian random variable (Box-Muller transform)
     */
    static gaussianRandom(mean = 0, stdDev = 1) {
        // Box-Muller transform
        let u1, u2, z;
        
        do {
            u1 = Math.random();
            u2 = Math.random();
        } while (u1 === 0); // Avoid log(0)

        z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);

        return mean + stdDev * z;
    }

    /**
     * Calculate theoretical BER for BPSK/QPSK in AWGN
     */
    static theoreticalBER_BPSK(ebN0DB) {
        const ebN0 = Math.pow(10, ebN0DB / 10);
        return 0.5 * this.erfc(Math.sqrt(ebN0));
    }

    /**
     * Complementary error function approximation
     */
    static erfc(x) {
        // Abramowitz and Stegun approximation
        const t = 1 / (1 + 0.3275911 * Math.abs(x));
        const a1 = 0.254829592;
        const a2 = -0.284496736;
        const a3 = 1.421413741;
        const a4 = -1.453152027;
        const a5 = 1.061405429;

        const erf = 1 - (a1 * t + a2 * t * t + a3 * t * t * t + 
                         a4 * t * t * t * t + a5 * t * t * t * t * t) * 
                         Math.exp(-x * x);

        return x >= 0 ? 1 - erf : 1 + erf;
    }

    /**
     * Calculate SNR from received symbols
     */
    static measureSNR(transmitted, received) {
        if (transmitted.length !== received.length) {
            throw new Error('Symbol arrays must have same length');
        }

        let signalPower = 0;
        let noisePower = 0;

        for (let i = 0; i < transmitted.length; i++) {
            const tx = transmitted[i];
            const rx = received[i];

            // Signal power
            signalPower += tx.real * tx.real + tx.imag * tx.imag;

            // Noise power (error)
            const errReal = rx.real - tx.real;
            const errImag = rx.imag - tx.imag;
            noisePower += errReal * errReal + errImag * errImag;
        }

        signalPower /= transmitted.length;
        noisePower /= transmitted.length;

        const snr = signalPower / noisePower;
        return 10 * Math.log10(snr);
    }
}
