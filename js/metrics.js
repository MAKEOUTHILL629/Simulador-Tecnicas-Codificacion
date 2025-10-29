// Performance Metrics

/**
 * Calculate various performance metrics
 */
export class Metrics {
    /**
     * Bit Error Rate
     */
    static calculateBER(transmitted, received) {
        if (transmitted.length !== received.length) {
            return null;
        }

        let errors = 0;
        for (let i = 0; i < transmitted.length; i++) {
            if (transmitted[i] !== received[i]) {
                errors++;
            }
        }

        return transmitted.length > 0 ? errors / transmitted.length : 0;
    }

    /**
     * Symbol Error Rate
     */
    static calculateSER(transmitted, received, bitsPerSymbol) {
        if (transmitted.length !== received.length) {
            return null;
        }

        let symbolErrors = 0;
        for (let i = 0; i < transmitted.length; i += bitsPerSymbol) {
            let symbolError = false;
            for (let j = 0; j < bitsPerSymbol && i + j < transmitted.length; j++) {
                if (transmitted[i + j] !== received[i + j]) {
                    symbolError = true;
                    break;
                }
            }
            if (symbolError) symbolErrors++;
        }

        const numSymbols = Math.ceil(transmitted.length / bitsPerSymbol);
        return numSymbols > 0 ? symbolErrors / numSymbols : 0;
    }

    /**
     * Peak Signal-to-Noise Ratio for images
     */
    static calculatePSNR(original, reconstructed) {
        const mse = this.calculateMSE(original, reconstructed);
        if (mse === 0) return Infinity;

        const maxPixel = 255;
        return 10 * Math.log10((maxPixel * maxPixel) / mse);
    }

    /**
     * Mean Squared Error
     */
    static calculateMSE(original, reconstructed) {
        if (original.length !== reconstructed.length) {
            throw new Error('Arrays must have same length');
        }

        let sumSquaredError = 0;
        for (let i = 0; i < original.length; i++) {
            const error = original[i] - reconstructed[i];
            sumSquaredError += error * error;
        }

        return sumSquaredError / original.length;
    }

    /**
     * Structural Similarity Index
     */
    static calculateSSIM(img1, img2, windowSize = 8) {
        // Simplified SSIM calculation
        // In production, would use proper windowing
        const k1 = 0.01;
        const k2 = 0.03;
        const L = 255; // Dynamic range
        const c1 = (k1 * L) ** 2;
        const c2 = (k2 * L) ** 2;

        // Calculate means
        const mu1 = this.mean(img1);
        const mu2 = this.mean(img2);

        // Calculate variances and covariance
        const sigma1sq = this.variance(img1, mu1);
        const sigma2sq = this.variance(img2, mu2);
        const sigma12 = this.covariance(img1, img2, mu1, mu2);

        // SSIM formula
        const numerator = (2 * mu1 * mu2 + c1) * (2 * sigma12 + c2);
        const denominator = (mu1 * mu1 + mu2 * mu2 + c1) * (sigma1sq + sigma2sq + c2);

        return numerator / denominator;
    }

    /**
     * Calculate mean
     */
    static mean(arr) {
        return arr.reduce((a, b) => a + b, 0) / arr.length;
    }

    /**
     * Calculate variance
     */
    static variance(arr, mean) {
        const sumSq = arr.reduce((sum, val) => sum + (val - mean) ** 2, 0);
        return sumSq / arr.length;
    }

    /**
     * Calculate covariance
     */
    static covariance(arr1, arr2, mean1, mean2) {
        let sum = 0;
        for (let i = 0; i < arr1.length; i++) {
            sum += (arr1[i] - mean1) * (arr2[i] - mean2);
        }
        return sum / arr1.length;
    }

    /**
     * Segmental SNR for audio
     */
    static calculateSegmentalSNR(original, reconstructed, frameSize = 882) {
        // 882 samples = 20ms at 44.1kHz
        const numFrames = Math.floor(original.length / frameSize);
        let sumLogSNR = 0;

        for (let f = 0; f < numFrames; f++) {
            const start = f * frameSize;
            const end = start + frameSize;

            let signalPower = 0;
            let noisePower = 0;

            for (let i = start; i < end; i++) {
                signalPower += original[i] * original[i];
                const noise = original[i] - reconstructed[i];
                noisePower += noise * noise;
            }

            if (noisePower > 0 && signalPower > 0) {
                const snr = signalPower / noisePower;
                sumLogSNR += 10 * Math.log10(snr);
            }
        }

        return numFrames > 0 ? sumLogSNR / numFrames : 0;
    }

    /**
     * Error Vector Magnitude (EVM)
     */
    static calculateEVM(ideal, received) {
        let errorPower = 0;
        let referencePower = 0;

        for (let i = 0; i < ideal.length; i++) {
            const errReal = received[i].real - ideal[i].real;
            const errImag = received[i].imag - ideal[i].imag;
            errorPower += errReal * errReal + errImag * errImag;

            referencePower += ideal[i].real * ideal[i].real + ideal[i].imag * ideal[i].imag;
        }

        errorPower /= ideal.length;
        referencePower /= ideal.length;

        return Math.sqrt(errorPower / referencePower) * 100; // Percentage
    }

    /**
     * Block Error Rate
     */
    static calculateBLER(transmitted, received, blockSize) {
        const numBlocks = Math.ceil(transmitted.length / blockSize);
        let blockErrors = 0;

        for (let b = 0; b < numBlocks; b++) {
            const start = b * blockSize;
            const end = Math.min(start + blockSize, transmitted.length);

            let hasError = false;
            for (let i = start; i < end; i++) {
                if (transmitted[i] !== received[i]) {
                    hasError = true;
                    break;
                }
            }

            if (hasError) blockErrors++;
        }

        return blockErrors / numBlocks;
    }

    /**
     * Levenshtein Distance for text
     */
    static levenshteinDistance(str1, str2) {
        const m = str1.length;
        const n = str2.length;
        const dp = Array(m + 1).fill(0).map(() => Array(n + 1).fill(0));

        for (let i = 0; i <= m; i++) dp[i][0] = i;
        for (let j = 0; j <= n; j++) dp[0][j] = j;

        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (str1[i - 1] === str2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        dp[i - 1][j],     // deletion
                        dp[i][j - 1],     // insertion
                        dp[i - 1][j - 1]  // substitution
                    );
                }
            }
        }

        return dp[m][n];
    }
}
