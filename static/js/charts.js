function getChartLayout(title) {
    const isDark = document.body.classList.contains('dark-mode');
    return {
        title: { text: title, font: { color: isDark ? '#F8FAFC' : '#0F172A', size: 18 } },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: isDark ? '#94A3B8' : '#64748B', family: 'Inter' },
        xaxis: { gridcolor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)' },
        yaxis: { gridcolor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)' },
        margin: { t: 50, l: 50, r: 20, b: 50 }
    };
}

async function renderDashboardCharts() {
    try {
        const response = await fetch('/api/dashboard/data');
        const data = await response.json();
        
        if (data.error) throw new Error(data.error);

        // Airline vs Price Chart
        const airlines = Object.keys(data.airline_prices);
        const prices = Object.values(data.airline_prices);
        
        Plotly.newPlot('airline-chart', [{
            x: airlines,
            y: prices,
            type: 'bar',
            marker: {
                color: '#2563EB',
                line: { width: 0 }
            }
        }], getChartLayout('Average Price by Airline'), {responsive: true});

        // Source Distribution
        const sources = Object.keys(data.source_distribution);
        const sourceCounts = Object.values(data.source_distribution);
        
        Plotly.newPlot('source-chart', [{
            labels: sources,
            values: sourceCounts,
            type: 'pie',
            hole: 0.4,
            marker: { colors: ['#2563EB', '#06B6D4', '#8B5CF6', '#F59E0B', '#10B981'] }
        }], getChartLayout('Source City Distribution'), {responsive: true});

        // Destination Distribution
        const dests = Object.keys(data.destination_distribution);
        const destCounts = Object.values(data.destination_distribution);
        
        Plotly.newPlot('dest-chart', [{
            labels: dests,
            values: destCounts,
            type: 'pie',
            hole: 0.4,
            marker: { colors: ['#8B5CF6', '#10B981', '#F59E0B', '#2563EB', '#06B6D4'] }
        }], getChartLayout('Destination Distribution'), {responsive: true});

        // Listen for theme changes to redraw
        window.addEventListener('themeChanged', () => {
            Plotly.relayout('airline-chart', getChartLayout('Average Price by Airline'));
            Plotly.relayout('source-chart', getChartLayout('Source City Distribution'));
            Plotly.relayout('dest-chart', getChartLayout('Destination Distribution'));
        });

    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

if (document.getElementById('airline-chart')) {
    renderDashboardCharts();
}
