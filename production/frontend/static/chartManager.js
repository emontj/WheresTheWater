// Copyright @emontj 2024

class ChartManager {
    constructor(canvasId, type = 'line') {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error(`Canvas with id '${canvasId}' not found.`);
            return;
        }
        this.type = type;
        this.chart = this.initializeChart();
    }

    initializeChart() {
        return new Chart(this.canvas.getContext('2d'), {
            type: this.type,
            data: {
                labels: ['Category 1', 'Category 2', 'Category 3'],
                datasets: [{
                    label: 'Occurrences as Subject',
                    data: [1, 1, 1],
                    backgroundColor: this.getBackgroundColors(),
                    borderColor: this.getBorderColors(),
                    borderWidth: 1,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#fff' } },
                },
                scales: this.type === 'pie' ? {} : {
                    y: {
                        beginAtZero: true,
                        grid: { color: '#444' },
                        ticks: { color: '#fff' },
                    },
                    x: {
                        grid: { color: '#444' },
                        ticks: { color: '#fff' },
                    }
                }
            }
        });
    }

    getBackgroundColors() {
        return ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)'];
    }

    getBorderColors() {
        return ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)'];
    }

    update(newData, newLabels = null) {
        if (!this.chart) return;
        this.chart.data.datasets[0].data = newData;
        if (newLabels) {
            this.chart.data.labels = newLabels;
        }
        this.chart.update();
    }
}

function updateMainCharts() {
    const individualsChart = new ChartManager('individualsChart', 'pie');
    const topicsChart = new ChartManager('topicsChart', 'pie');

    fetch('/counts')
        .then(response => response.json())
        .then(data => {
            for (const [key, value] of Object.entries(data)) {
                const labels = Object.values(value);
                const counts = Object.keys(value);

                if (key === 'Individuals') {
                    individualsChart.update(labels, counts);
                } else if (key === 'Topics') {
                    topicsChart.update(labels, counts);
                }
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}


document.addEventListener('DOMContentLoaded', () => {
    // For reference
    // const lineChartManager = new ChartManager('lineChart', 'line');
    // document.getElementById('updateLineChartButton')?.addEventListener('click', () => {
    //     const newData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 100));
    //     lineChartManager.update(newData, newData.map((_, i) => `Item ${i + 1}`));
    // });

    // const pieChartManager = new ChartManager('pieChart', 'pie');
    // document.getElementById('updatePieChartButton')?.addEventListener('click', () => {
    //     const newData = Array.from({ length: 3 }, () => Math.floor(Math.random() * 100));
    //     const newLabels = ['Category A', 'Category B', 'Category C'];
    //     pieChartManager.update(newData, newLabels);
    // });

    updateMainCharts();
});
