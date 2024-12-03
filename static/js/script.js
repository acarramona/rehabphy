document.addEventListener("DOMContentLoaded", function () {
    
    let charts = {};

    // function to convert text to slug form for use in IDs
    function slugify(text) {
        return text.toString().toLowerCase()
            .replace(/\s+/g, '-')           // Replace spaces with -
            .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
            .replace(/\-\-+/g, '-')         // Replace multiple - with single -
            .replace(/^-+/, '')             // Trim - from start of text
            .replace(/-+$/, '');            // Trim - from end of text
    }

    // Pain Chart Initialization
    const painChartContext = document.getElementById('painData');
    if (painChartContext) {
        let painData;

        try {
            painData = JSON.parse(painChartContext.textContent);
        } catch (e) {
            console.error('Error parsing painData: ', e);
            painData = {};
        }

        if (painData &&
            Array.isArray(painData.dates) && painData.dates.length > 0 &&
            Array.isArray(painData.pain_levels) && painData.pain_levels.length > 0) {
            
            drawPainChart(painData);
        } else {
            console.error('Pain data is not in the expected format or is missing required fields.');
        }
    }

    function drawPainChart(painData) {
        const ctx = document.getElementById('painChart');

        if (ctx) {
            // Destroy the previous chart if it exists to avoid canvas reuse errors
            if (charts['painChart']) {
                charts['painChart'].destroy();
            }

            const chartContext = ctx.getContext('2d');
            charts['painChart'] = new Chart(chartContext, {
                type: 'line',
                data: {
                    labels: painData.dates,
                    datasets: [{
                        label: 'Pain Level',
                        data: painData.pain_levels,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        fill: true,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 10
                        }
                    }
                }
            });
        }
    }

    // Range of Motion (ROM) Chart Initialization
    const romDataContext = document.getElementById('romData');
    if (romDataContext) {
        let romData;
        try {
            romData = JSON.parse(romDataContext.textContent);
        } catch (e) {
            console.error('Error parsing romData:', e);
            romData = [];
        }

        if (Array.isArray(romData) && romData.length > 0) {
            drawRomCharts(romData);
        } else {
            console.error('ROM data is not a valid format or is empty.');
        }
    }

    function drawRomCharts(romData) {
        // Iterate through each ROM data entry to create a chart
        romData.forEach((romEntry) => {
            if (romEntry &&
                romEntry.joint &&
                Array.isArray(romEntry.dates) && romEntry.dates.length > 0 &&
                Array.isArray(romEntry.assessed_values) && romEntry.assessed_values.length > 0 &&
                Array.isArray(romEntry.expected_values) && romEntry.expected_values.length > 0) {

                const slugifiedKey = slugify(romEntry.joint);
                const containerId = `chart-${slugifiedKey}`;

                // Create container for chart if it doesn't exist
                let container = document.getElementById(containerId);
                if (!container) {
                    container = document.createElement('canvas');
                    container.id = containerId;
                    container.style.width = "100%";
                    container.style.height = "300px";
                    const romChartsContainer = document.getElementById('romChartsContainer');

                    // To ensure the container exists before appending the new canvas
                    if (romChartsContainer) {
                        romChartsContainer.appendChild(container);
                    } else {
                        console.error('romChartsContainer not found. Cannot append ROM charts.');
                        return;
                    }
                }

                const ctx = container.getContext('2d');

                // Destroy the previous chart if it exists to avoid canvas reuse errors
                if (charts[containerId]) {
                    charts[containerId].destroy();
                }

                // Create new chart instance
                charts[containerId] = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: romEntry.dates,
                        datasets: [
                            {
                                label: 'Assessed Value',
                                data: romEntry.assessed_values,
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                fill: true,
                            },
                            {
                                label: 'Expected Value',
                                data: romEntry.expected_values,
                                borderColor: 'rgba(153, 102, 255, 1)',
                                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                                fill: true,
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            } else {
                console.warn('Invalid ROM entry:', romEntry);
            }
        });
    }
});
