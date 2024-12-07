class ChartManager {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = this.initializeChart();
    }

    initializeChart() {
        return new Chart(this.canvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'],
                datasets: [{
                    label: 'Dataset 1',
                    data: [10, 20, 30, 40, 50], // Default data
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                }]
            },
            options: {
                responsive: true,
                animation: {
                    duration: 1000,
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    update(newData) {
        this.chart.data.datasets[0].data = newData;
        this.chart.data.labels = newData.map((_, i) => `Item ${i + 1}`);
        this.chart.update();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const chartManager = new ChartManager('myChart');

    document.getElementById('updateButton').addEventListener('click', () => {
        const newData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 100)); // TODO: Random data
        chartManager.update(newData);
    });
});
