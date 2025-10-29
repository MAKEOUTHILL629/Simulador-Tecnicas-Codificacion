// Visualization using Plotly.js

/**
 * Visualization utilities
 */
export class Visualizer {
    /**
     * Plot constellation diagram
     */
    static plotConstellation(symbols, elementId, title = 'Diagrama de Constelación') {
        try {
            if (typeof Plotly === 'undefined') {
                // Fallback to text description
                const element = document.getElementById(elementId);
                element.innerHTML = `
                    <div style="padding: 1rem; text-align: center;">
                        <strong>${title}</strong>
                        <p class="info-text">${symbols.length} símbolos modulados</p>
                        <p class="info-text">Rango I: [${Math.min(...symbols.map(s => s.real)).toFixed(2)}, ${Math.max(...symbols.map(s => s.real)).toFixed(2)}]</p>
                        <p class="info-text">Rango Q: [${Math.min(...symbols.map(s => s.imag)).toFixed(2)}, ${Math.max(...symbols.map(s => s.imag)).toFixed(2)}]</p>
                    </div>
                `;
                return;
            }
            
            const real = symbols.map(s => s.real);
            const imag = symbols.map(s => s.imag);

        const trace = {
            x: real,
            y: imag,
            mode: 'markers',
            type: 'scatter',
            marker: {
                size: 4,
                color: 'rgba(37, 99, 235, 0.6)',
                line: {
                    color: 'rgba(37, 99, 235, 1)',
                    width: 1
                }
            },
            name: 'Símbolos'
        };

        const layout = {
            title: title,
            xaxis: {
                title: 'In-Phase (I)',
                zeroline: true,
                showgrid: true
            },
            yaxis: {
                title: 'Quadrature (Q)',
                zeroline: true,
                showgrid: true
            },
            width: null,
            height: 300,
            margin: { l: 50, r: 30, t: 40, b: 50 },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(248,250,252,1)'
        };

        const config = {
            responsive: true,
            displayModeBar: false
        };

        Plotly.newPlot(elementId, [trace], layout, config);
    }

    /**
     * Plot constellation with ideal points overlay
     */
    static plotConstellationWithIdeal(received, ideal, elementId, title = 'Señal Recibida') {
        try {
            if (typeof Plotly === 'undefined') {
                // Fallback
                const element = document.getElementById(elementId);
                element.innerHTML = `
                    <div style="padding: 1rem; text-align: center;">
                        <strong>${title}</strong>
                        <p class="info-text">${received.length} símbolos recibidos</p>
                        <p class="info-text">Con ruido del canal aplicado</p>
                    </div>
                `;
                return;
            }
            
            const receivedTrace = {
            x: received.map(s => s.real),
            y: received.map(s => s.imag),
            mode: 'markers',
            type: 'scatter',
            marker: {
                size: 3,
                color: 'rgba(239, 68, 68, 0.4)',
            },
            name: 'Recibido'
        };

        const idealTrace = {
            x: ideal.map(s => s.real),
            y: ideal.map(s => s.imag),
            mode: 'markers',
            type: 'scatter',
            marker: {
                size: 8,
                color: 'rgba(16, 185, 129, 1)',
                symbol: 'x',
                line: {
                    width: 2
                }
            },
            name: 'Ideal'
        };

        const layout = {
            title: title,
            xaxis: {
                title: 'In-Phase (I)',
                zeroline: true,
                showgrid: true
            },
            yaxis: {
                title: 'Quadrature (Q)',
                zeroline: true,
                showgrid: true
            },
            width: null,
            height: 300,
            margin: { l: 50, r: 30, t: 40, b: 50 },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(248,250,252,1)',
            showlegend: true,
            legend: { x: 0.02, y: 0.98 }
        };

        const config = {
            responsive: true,
            displayModeBar: false
        };

        Plotly.newPlot(elementId, [receivedTrace, idealTrace], layout, config);
    }

    /**
     * Plot LLR histogram
     */
    static plotLLRHistogram(llrs, elementId) {
        try {
            if (typeof Plotly === 'undefined') {
                // Fallback
                const element = document.getElementById(elementId);
                const avg = llrs.reduce((a, b) => a + b, 0) / llrs.length;
                const min = Math.min(...llrs);
                const max = Math.max(...llrs);
                element.innerHTML = `
                    <div style="padding: 1rem; text-align: center;">
                        <strong>Distribución de LLRs</strong>
                        <p class="info-text">${llrs.length} LLRs calculados</p>
                        <p class="info-text">Rango: [${min.toFixed(2)}, ${max.toFixed(2)}]</p>
                        <p class="info-text">Promedio: ${avg.toFixed(2)}</p>
                    </div>
                `;
                return;
            }
            
            const trace = {
            x: llrs,
            type: 'histogram',
            nbinsx: 50,
            marker: {
                color: 'rgba(37, 99, 235, 0.7)',
                line: {
                    color: 'rgba(37, 99, 235, 1)',
                    width: 1
                }
            },
            name: 'LLRs'
        };

        const layout = {
            title: 'Distribución de LLRs',
            xaxis: {
                title: 'Valor LLR',
                showgrid: true
            },
            yaxis: {
                title: 'Frecuencia',
                showgrid: true
            },
            width: null,
            height: 250,
            margin: { l: 50, r: 30, t: 40, b: 50 },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(248,250,252,1)'
        };

        const config = {
            responsive: true,
            displayModeBar: false
        };

        Plotly.newPlot(elementId, [trace], layout, config);
    }

    /**
     * Plot audio waveform
     */
    static plotWaveform(time, amplitude, elementId, title = 'Forma de Onda de Audio') {
        const trace = {
            x: time,
            y: amplitude,
            type: 'scatter',
            mode: 'lines',
            line: {
                color: 'rgba(37, 99, 235, 0.8)',
                width: 1
            },
            name: 'Amplitud'
        };

        const layout = {
            title: title,
            xaxis: {
                title: 'Tiempo (s)',
                showgrid: true
            },
            yaxis: {
                title: 'Amplitud',
                showgrid: true
            },
            width: null,
            height: 250,
            margin: { l: 50, r: 30, t: 40, b: 50 },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(248,250,252,1)'
        };

        const config = {
            responsive: true,
            displayModeBar: false
        };

        Plotly.newPlot(elementId, [trace], layout, config);
    }

    /**
     * Plot BER vs SNR curve
     */
    static plotBERCurve(snrValues, berValues, elementId) {
        const trace = {
            x: snrValues,
            y: berValues,
            type: 'scatter',
            mode: 'lines+markers',
            line: {
                color: 'rgba(37, 99, 235, 1)',
                width: 2
            },
            marker: {
                size: 6
            },
            name: 'BER'
        };

        const layout = {
            title: 'BER vs SNR',
            xaxis: {
                title: 'SNR (dB)',
                showgrid: true
            },
            yaxis: {
                title: 'BER',
                type: 'log',
                showgrid: true
            },
            width: null,
            height: 300,
            margin: { l: 60, r: 30, t: 40, b: 50 },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(248,250,252,1)'
        };

        const config = {
            responsive: true,
            displayModeBar: false
        };

        Plotly.newPlot(elementId, [trace], layout, config);
    }

    /**
     * Display image in canvas
     */
    static displayImage(imageData, canvasId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        canvas.width = imageData.width;
        canvas.height = imageData.height;
        const ctx = canvas.getContext('2d');
        ctx.putImageData(imageData, 0, 0);
    }

    /**
     * Display text
     */
    static displayText(text, elementId) {
        const element = document.getElementById(elementId);
        if (!element) return;

        element.textContent = text;
    }

    /**
     * Display binary data (first N bits)
     */
    static displayBinary(binary, elementId, maxBits = 200) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const truncated = binary.slice(0, maxBits);
        const formatted = truncated.match(/.{1,8}/g).join(' ');
        
        element.innerHTML = `
            <pre class="bits-display">${formatted}${binary.length > maxBits ? '...' : ''}</pre>
            <p class="info-text">Mostrando ${Math.min(maxBits, binary.length)} de ${binary.length} bits</p>
        `;
    }
}
