// Information Theory Calculations

/**
 * Information theory utilities
 */
export class InformationTheory {
    /**
     * Calculate entropy of a discrete source
     */
    static calculateEntropy(data) {
        // Build frequency table
        const freq = {};
        for (const symbol of data) {
            freq[symbol] = (freq[symbol] || 0) + 1;
        }

        // Calculate probabilities and entropy
        const total = data.length;
        let entropy = 0;

        for (const count of Object.values(freq)) {
            const p = count / total;
            if (p > 0) {
                entropy -= p * Math.log2(p);
            }
        }

        return entropy;
    }

    /**
     * Calculate joint entropy H(X,Y)
     */
    static calculateJointEntropy(dataX, dataY) {
        if (dataX.length !== dataY.length) {
            throw new Error('Data arrays must have same length');
        }

        // Build joint frequency table
        const jointFreq = {};
        for (let i = 0; i < dataX.length; i++) {
            const key = `${dataX[i]},${dataY[i]}`;
            jointFreq[key] = (jointFreq[key] || 0) + 1;
        }

        // Calculate joint entropy
        const total = dataX.length;
        let entropy = 0;

        for (const count of Object.values(jointFreq)) {
            const p = count / total;
            if (p > 0) {
                entropy -= p * Math.log2(p);
            }
        }

        return entropy;
    }

    /**
     * Calculate conditional entropy H(X|Y)
     */
    static calculateConditionalEntropy(dataX, dataY) {
        const hXY = this.calculateJointEntropy(dataX, dataY);
        const hY = this.calculateEntropy(dataY);
        return hXY - hY;
    }

    /**
     * Calculate mutual information I(X;Y)
     */
    static calculateMutualInformation(dataX, dataY) {
        if (dataX.length !== dataY.length) {
            throw new Error('Data arrays must have same length');
        }

        const hX = this.calculateEntropy(dataX);
        const hY = this.calculateEntropy(dataY);
        const hXY = this.calculateJointEntropy(dataX, dataY);

        // I(X;Y) = H(X) + H(Y) - H(X,Y)
        return hX + hY - hXY;
    }

    /**
     * Alternative mutual information calculation using joint distribution
     */
    static calculateMutualInformationDirect(dataX, dataY) {
        if (dataX.length !== dataY.length) {
            throw new Error('Data arrays must have same length');
        }

        // Build frequency tables
        const freqX = {};
        const freqY = {};
        const jointFreq = {};

        for (let i = 0; i < dataX.length; i++) {
            const x = dataX[i];
            const y = dataY[i];
            const key = `${x},${y}`;

            freqX[x] = (freqX[x] || 0) + 1;
            freqY[y] = (freqY[y] || 0) + 1;
            jointFreq[key] = (jointFreq[key] || 0) + 1;
        }

        // Calculate mutual information
        const total = dataX.length;
        let mi = 0;

        for (const [key, count] of Object.entries(jointFreq)) {
            const [x, y] = key.split(',');
            const pXY = count / total;
            const pX = freqX[x] / total;
            const pY = freqY[y] / total;

            if (pXY > 0 && pX > 0 && pY > 0) {
                mi += pXY * Math.log2(pXY / (pX * pY));
            }
        }

        return mi;
    }

    /**
     * Calculate channel capacity (Shannon capacity)
     */
    static channelCapacity(snr) {
        // C = log2(1 + SNR) bits per channel use
        // SNR should be linear (not dB)
        return Math.log2(1 + snr);
    }

    /**
     * Calculate channel capacity from SNR in dB
     */
    static channelCapacityDB(snrDB) {
        const snr = Math.pow(10, snrDB / 10);
        return this.channelCapacity(snr);
    }

    /**
     * Calculate compression ratio
     */
    static compressionRatio(originalSize, compressedSize) {
        return originalSize / compressedSize;
    }

    /**
     * Calculate redundancy
     */
    static redundancy(entropy, maxEntropy) {
        // Redundancy = 1 - (H / H_max)
        return 1 - (entropy / maxEntropy);
    }

    /**
     * Calculate relative entropy (KL divergence)
     */
    static kullbackLeiblerDivergence(p, q) {
        if (p.length !== q.length) {
            throw new Error('Distributions must have same length');
        }

        let kl = 0;
        for (let i = 0; i < p.length; i++) {
            if (p[i] > 0 && q[i] > 0) {
                kl += p[i] * Math.log2(p[i] / q[i]);
            }
        }

        return kl;
    }

    /**
     * Estimate probability distribution from data
     */
    static estimateDistribution(data) {
        const freq = {};
        for (const symbol of data) {
            freq[symbol] = (freq[symbol] || 0) + 1;
        }

        const total = data.length;
        const distribution = {};

        for (const [symbol, count] of Object.entries(freq)) {
            distribution[symbol] = count / total;
        }

        return distribution;
    }

    /**
     * Calculate information rate
     */
    static informationRate(entropy, symbolRate) {
        // Information rate = entropy × symbol rate (bits/second)
        return entropy * symbolRate;
    }

    /**
     * Calculate coding efficiency
     */
    static codingEfficiency(entropy, avgCodeLength) {
        // Efficiency = H / L
        return entropy / avgCodeLength;
    }

    /**
     * Calculate theoretical minimum bits (entropy bound)
     */
    static theoreticalMinimumBits(data) {
        const entropy = this.calculateEntropy(data);
        return entropy * data.length;
    }
}
