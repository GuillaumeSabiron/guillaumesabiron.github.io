function initializeChart() {
    const ctx = document.getElementById('myStackedChart').getContext('2d');
    const myStackedChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['2012','2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'],
            datasets: [
                {
                    label: 'Conference Papers',
                    data: [0, 2, 3, 1, 2, 2, 3, 3, 1, 2, 3, 4],
                    backgroundColor: 'rgba(30, 144, 255, 0.7)',
                },
                {
                    label: 'Journal Articles',
                    data: [1, 1, 0, 1, 1, 0, 2, 0, 3, 2, 0, 2],
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                },
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: false,
                    text: 'Papers Published Per Year'
                }
            },
            scales: {
                x: {
                    stacked: true, // Enable stacking on the x-axis
                },
                y: {
                    stacked: true, // Enable stacking on the y-axis
                }
            }
        }
    });
}
