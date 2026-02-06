document.addEventListener('DOMContentLoaded', () => {
    fetchSustainabilityData();
});

async function fetchSustainabilityData() {
    const dashboard = document.getElementById('dashboard-content');
    const loading = document.getElementById('loading');

    try {
        const response = await fetch('/sustainability/context');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        // Hide loading, show dashboard
        loading.style.display = 'none';
        dashboard.style.display = 'block';

        renderInternalMetrics(data.internal_sustainability_metrics);
        renderExternalContext(data.external_carbon_context);

    } catch (error) {
        console.error('Error fetching data:', error);
        loading.innerHTML = '<p style="color: red; text-align: center;">Failed to load data. Please try again later.</p>';
    }
}

function renderInternalMetrics(metrics) {
    // Top Level Metrics
    document.getElementById('total-usage').textContent = `${metrics.total_resource_usage.toLocaleString()} units`;

    const renewablePct = (metrics.renewable_usage / metrics.total_resource_usage * 100).toFixed(1);
    document.getElementById('renewable-pct').textContent = `${renewablePct}%`;
    document.getElementById('renewable-sub').textContent = `${metrics.renewable_usage} units`;

    const nonRenewablePct = (metrics.non_renewable_usage / metrics.total_resource_usage * 100).toFixed(1);
    document.getElementById('non-renewable-pct').textContent = `${nonRenewablePct}%`;
    document.getElementById('non-renewable-sub').textContent = `${metrics.non_renewable_usage} units`;

    // Resource Breakdown HTML generation
    const breakdownContainer = document.getElementById('resource-breakdown');
    breakdownContainer.innerHTML = ''; // Clear previous

    metrics.resource_breakdown.forEach(res => {
        const div = document.createElement('div');
        div.className = 'metric-card';
        div.innerHTML = `
            <h3>${res.name}</h3>
            <div class="metric-value">${res.usage_percent}%</div>
            <p class="metric-sub">${res.used} / ${res.total} used</p>
            <p style="color: ${res.renewable ? 'green' : 'gray'}; font-weight: bold;">
                ${res.renewable ? 'Renewable' : 'Non-Renewable'}
            </p>
        `;
        breakdownContainer.appendChild(div);
    });

    // Alerts
    const alertBox = document.getElementById('alerts');
    if (metrics.alerts && metrics.alerts.length > 0) {
        alertBox.style.display = 'block';
        alertBox.innerHTML = '<strong>Alerts:</strong><br>' + metrics.alerts.join('<br>');
    } else {
        alertBox.style.display = 'none';
    }

    // Recommendation
    const recBox = document.getElementById('recommendation');
    recBox.innerHTML = `<strong>Recommendation:</strong> ${metrics.recommendation}`;
}

function renderExternalContext(context) {
    const container = document.getElementById('external-context');

    if (context.status === 'success' && context.data) {
        container.innerHTML = `
            <div class="metric-card" style="width: 100%;">
                <h3>Carbon Emission Context (US)</h3>
                <p>${context.description}</p>
                <div class="dashboard-grid" style="justify-content: center;">
                    <div style="margin: 0 20px;">
                        <span class="metric-value">${context.data.co2e.toFixed(2)}</span>
                        <span class="metric-sub">${context.data.co2e_unit} CO2e</span>
                        <p>Total Emissions</p>
                    </div>
                </div>
                <p class="metric-sub" style="margin-top: 10px;">Source: Climatiq API</p>
            </div>
        `;
    } else if (context.error) {
        container.innerHTML = `
            <div class="metric-card" style="width: 100%; border-left: 5px solid orange;">
                <h3>External Data Unavailable</h3>
                <p>${context.error}</p>
                <p class="metric-sub">${context.description}</p>
            </div>
        `;
    }
}
