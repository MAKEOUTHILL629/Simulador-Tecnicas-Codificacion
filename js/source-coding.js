// Source Coding Algorithms

/**
 * Huffman Coding Implementation
 */
export class HuffmanCoder {
    constructor() {
        this.tree = null;
        this.codeTable = {};
    }

    /**
     * Build Huffman tree from data
     */
    buildTree(data) {
        // Calculate frequencies
        const freq = {};
        for (const symbol of data) {
            freq[symbol] = (freq[symbol] || 0) + 1;
        }

        // Create initial nodes
        const nodes = Object.entries(freq).map(([symbol, frequency]) => ({
            symbol,
            frequency,
            left: null,
            right: null
        }));

        // Build tree
        while (nodes.length > 1) {
            // Sort by frequency
            nodes.sort((a, b) => a.frequency - b.frequency);

            // Take two nodes with lowest frequency
            const left = nodes.shift();
            const right = nodes.shift();

            // Create parent node
            const parent = {
                symbol: null,
                frequency: left.frequency + right.frequency,
                left,
                right
            };

            nodes.push(parent);
        }

        this.tree = nodes[0];
        this.generateCodeTable(this.tree, '');
    }

    /**
     * Generate code table from tree
     */
    generateCodeTable(node, code) {
        if (!node) return;

        if (node.symbol !== null) {
            this.codeTable[node.symbol] = code || '0';
        } else {
            this.generateCodeTable(node.left, code + '0');
            this.generateCodeTable(node.right, code + '1');
        }
    }

    /**
     * Encode data using Huffman coding
     */
    encode(data) {
        this.buildTree(data);

        let encoded = '';
        for (const symbol of data) {
            encoded += this.codeTable[symbol];
        }

        return {
            encoded,
            codeTable: this.codeTable,
            tree: this.tree,
            originalLength: data.length,
            encodedLength: encoded.length
        };
    }

    /**
     * Decode Huffman encoded data
     */
    decode(encoded, tree) {
        let decoded = '';
        let currentNode = tree;

        for (const bit of encoded) {
            currentNode = bit === '0' ? currentNode.left : currentNode.right;

            if (currentNode.symbol !== null) {
                decoded += currentNode.symbol;
                currentNode = tree;
            }
        }

        return decoded;
    }
}

/**
 * DCT-based Image/Video Coding
 */
export class DCTCoder {
    /**
     * 2D DCT for 8x8 block
     */
    static dct2d(block) {
        const N = 8;
        const dct = Array(N).fill(0).map(() => Array(N).fill(0));

        for (let u = 0; u < N; u++) {
            for (let v = 0; v < N; v++) {
                let sum = 0;
                for (let x = 0; x < N; x++) {
                    for (let y = 0; y < N; y++) {
                        sum += block[x][y] *
                            Math.cos((2 * x + 1) * u * Math.PI / (2 * N)) *
                            Math.cos((2 * y + 1) * v * Math.PI / (2 * N));
                    }
                }
                const cu = u === 0 ? 1 / Math.sqrt(2) : 1;
                const cv = v === 0 ? 1 / Math.sqrt(2) : 1;
                dct[u][v] = 0.25 * cu * cv * sum;
            }
        }

        return dct;
    }

    /**
     * 2D IDCT for 8x8 block
     */
    static idct2d(dct) {
        const N = 8;
        const block = Array(N).fill(0).map(() => Array(N).fill(0));

        for (let x = 0; x < N; x++) {
            for (let y = 0; y < N; y++) {
                let sum = 0;
                for (let u = 0; u < N; u++) {
                    for (let v = 0; v < N; v++) {
                        const cu = u === 0 ? 1 / Math.sqrt(2) : 1;
                        const cv = v === 0 ? 1 / Math.sqrt(2) : 1;
                        sum += cu * cv * dct[u][v] *
                            Math.cos((2 * x + 1) * u * Math.PI / (2 * N)) *
                            Math.cos((2 * y + 1) * v * Math.PI / (2 * N));
                    }
                }
                block[x][y] = 0.25 * sum;
            }
        }

        return block;
    }

    /**
     * Quantization matrix (JPEG-like)
     */
    static getQuantizationMatrix(quality) {
        const base = [
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99]
        ];

        const scale = quality < 50 ? 5000 / quality : 200 - 2 * quality;

        return base.map(row =>
            row.map(val => Math.max(1, Math.floor((val * scale + 50) / 100)))
        );
    }

    /**
     * Zigzag scan order
     */
    static zigzagOrder() {
        return [
            [0,0], [0,1], [1,0], [2,0], [1,1], [0,2], [0,3], [1,2],
            [2,1], [3,0], [4,0], [3,1], [2,2], [1,3], [0,4], [0,5],
            [1,4], [2,3], [3,2], [4,1], [5,0], [6,0], [5,1], [4,2],
            [3,3], [2,4], [1,5], [0,6], [0,7], [1,6], [2,5], [3,4],
            [4,3], [5,2], [6,1], [7,0], [7,1], [6,2], [5,3], [4,4],
            [3,5], [2,6], [1,7], [2,7], [3,6], [4,5], [5,4], [6,3],
            [7,2], [7,3], [6,4], [5,5], [4,6], [3,7], [4,7], [5,6],
            [6,5], [7,4], [7,5], [6,6], [5,7], [6,7], [7,6], [7,7]
        ];
    }
}

/**
 * MDCT-based Audio Coding
 */
export class MDCTCoder {
    /**
     * Modified Discrete Cosine Transform
     */
    static mdct(samples, blockSize = 1024) {
        const N = blockSize;
        const coefficients = [];

        for (let k = 0; k < N / 2; k++) {
            let sum = 0;
            for (let n = 0; n < N; n++) {
                sum += samples[n] * Math.cos(Math.PI / N * (n + 0.5 + N / 4) * (k + 0.5));
            }
            coefficients.push(sum);
        }

        return coefficients;
    }

    /**
     * Inverse MDCT
     */
    static imdct(coefficients, blockSize = 1024) {
        const N = blockSize;
        const samples = new Array(N);

        for (let n = 0; n < N; n++) {
            let sum = 0;
            for (let k = 0; k < N / 2; k++) {
                sum += coefficients[k] * Math.cos(Math.PI / N * (n + 0.5 + N / 4) * (k + 0.5));
            }
            samples[n] = 2 / N * sum;
        }

        return samples;
    }
}
