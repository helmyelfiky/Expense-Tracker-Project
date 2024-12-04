document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById("categoryPieChart").getContext("2d");

    // Define a specific color for "Salary" or "salary"
    const salaryColor = "#1cc88a";

    // Function to convert hex color to RGB
    function hexToRgb(hex) {
        const bigint = parseInt(hex.slice(1), 16);
        const r = (bigint >> 16) & 255;
        // const g = (bigint >> 8) & 255;
        const g = 0;
        const b = bigint & 255;
        return [r, g, b];
    }

    // Function to calculate color difference
    function colorDifference(color1, color2) {
        const rgb1 = hexToRgb(color1);
        const rgb2 = hexToRgb(color2);
        return Math.sqrt(
            Math.pow(rgb1[0] - rgb2[0], 2) +
            Math.pow(rgb1[1] - rgb2[1], 2) +
            Math.pow(rgb1[2] - rgb2[2], 2)
        );
    }

    // Function to generate a random color that is sufficiently different from salaryColor
    function getRandomColor() {
        let color;
        do {
            const letters = '0123456789ABCDEF';
            color = '#';
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
        } while (colorDifference(color, salaryColor) < 100); // Adjust the threshold as needed
        return color;
    }

    // Generate the background colors array based on the chart labels
    const backgroundColors = chartLabels.map(label => {
        if (label.toLowerCase() === "salary") {
            return salaryColor;
        } else {
            return getRandomColor();
        }
    });

    console.log(chartLabels, chartData, backgroundColors);

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: chartLabels, // Category names
            datasets: [
                {
                    data: chartData, // Amounts spent
                    backgroundColor: backgroundColors, // Colors based on category
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            
            plugins: {
                legend: {
                    display: true, // Disable the default legend
                },
                tooltip: {
                    callbacks: {
                        label: (tooltipItem) => {
                            let sum = tooltipItem.dataset.data.reduce((a, b) => a + b, 0);
                            let percentage = (tooltipItem.raw * 100 / sum).toFixed(2) + "%";
                            return `${tooltipItem.label}: ${percentage}`;
                        }
                    }
                }
            },
            onAfterDraw: (chart) => {
                const ctx = chart.ctx;
                const { top, left, width, height } = chart.chartArea;
                const legendX = left + width + 20; // Position the legend to the right of the chart
                const legendY = top;

                ctx.textAlign = 'left';
                ctx.textBaseline = 'middle';
                ctx.font = '12px Arial';

                chart.data.labels.forEach((label, index) => {
                    const meta = chart.getDatasetMeta(0);
                    const total = meta.total;
                    const value = chart.data.datasets[0].data[index];
                    const percentage = ((value / total) * 100).toFixed(2) + '%';

                    ctx.fillStyle = chart.data.datasets[0].backgroundColor[index];
                    ctx.fillRect(legendX, legendY + index * 20, 10, 10);

                    ctx.fillStyle = '#000';
                    ctx.fillText(`${label}: ${percentage}`, legendX + 15, legendY + index * 20 + 5);
                });
            }
        }
    });

    // Display of chart 1
    const ctx1 = document.getElementById("categoryBarChart").getContext("2d");
    new Chart(ctx1, {
        type: "bar",
        data: {
            labels: chartLabels,
            datasets: [
                {
                    label: "Amount Spent",
                    data: chartData,
                    backgroundColor: backgroundColors,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
});

