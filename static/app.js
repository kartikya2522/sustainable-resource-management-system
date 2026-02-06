// Chart Global Defaults (Dark Mode)
Chart.defaults.font.family = "'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif";
Chart.defaults.color = '#94a3b8'; // Slate 400
Chart.defaults.borderColor = '#334155'; // Slate 700 (Grid lines)

document.addEventListener('DOMContentLoaded', () => {
    fetchSustainabilityData();
});

let mixChartInstance = null;
let usageChartInstance = null;

async function fetchSustainabilityData() {
    const dashboard = document.getElementById('dashboard-content');
    const loading = document.getElementById('loading');

    try {
        const response = await fetch('/sustainability/context');
        if (!response.ok) throw new Error('Network error');
        const data = await response.json();

        loading.style.display = 'none';
        dashboard.style.display = 'grid';

        updateKPIs(data.internal_sustainability_metrics, data.environmental_impact);
        renderCharts(data.internal_sustainability_metrics);
        renderMonitor(data.internal_sustainability_metrics);
        renderImpact(data.environmental_impact, data.internal_sustainability_metrics);

    } catch (error) {
        console.error(error);
        loading.innerHTML = `<div class="alert"><i class="fa-solid fa-triangle-exclamation"></i> System Disconnected. Check Console.</div>`;
    }
}

function updateKPIs(metrics, impact) {
    // Total
    document.getElementById('kpi-total').textContent = `${metrics.total_resource_usage.toLocaleString()}`;

    // Renewable %
    const renPct = (metrics.renewable_usage / metrics.total_resource_usage * 100).toFixed(1);
    const kpiRen = document.getElementById('kpi-renewable');
    kpiRen.textContent = `${renPct}%`;

    // Non-Renewable %
    const nonRenPct = (metrics.non_renewable_usage / metrics.total_resource_usage * 100).toFixed(1);
    document.getElementById('kpi-non-renewable').textContent = `${nonRenPct}%`;

    // Carbon
    if (impact.status === 'simulated_internal') {
        document.getElementById('kpi-carbon').textContent = `${impact.total_co2e.toLocaleString()}`;
    } else {
        document.getElementById('kpi-carbon').textContent = 'N/A';
    }
}

function renderCharts(metrics) {
    // 1. Energy Mix Donut Chart
    const ctxMix = document.getElementById('mixChart').getContext('2d');

    // Destroy if exists
    if (mixChartInstance) mixChartInstance.destroy();

    mixChartInstance = new Chart(ctxMix, {
        type: 'doughnut',
        data: {
            labels: ['Renewable', 'Non-Renewable'],
            datasets: [{
                data: [metrics.renewable_usage, metrics.non_renewable_usage],
                backgroundColor: ['#10b981', '#ef4444'], // Emerald, Red
                borderColor: '#1e293b', // Match panel bg
                borderWidth: 2,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#f8fafc' } // Light text
                }
            }
        }
    });

    // 2. Resource Usage Bar Chart
    const ctxUsage = document.getElementById('usageChart').getContext('2d');

    // Prepare Data
    const labels = metrics.resource_breakdown.map(r => r.name);
    const dataUsage = metrics.resource_breakdown.map(r => r.used);
    const colors = metrics.resource_breakdown.map(r => r.renewable ? '#3b82f6' : '#64748b'); // Blue vs Slate

    if (usageChartInstance) usageChartInstance.destroy();

    usageChartInstance = new Chart(ctxUsage, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Units Consumed',
                data: dataUsage,
                backgroundColor: colors,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#334155' }, // Subtle grid
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#f8fafc' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderMonitor(metrics) {
    const list = document.getElementById('resource-list');
    list.innerHTML = '';

    metrics.resource_breakdown.forEach(res => {
        // Icon logic
        let iconClass = 'fa-cube';
        if (res.name.toLowerCase().includes('water')) iconClass = 'fa-droplet';
        if (res.name.toLowerCase().includes('solar')) iconClass = 'fa-sun';
        if (res.name.toLowerCase().includes('coal')) iconClass = 'fa-fire-flame-curved';
        if (res.name.toLowerCase().includes('waste')) iconClass = 'fa-recycle';

        // Color logic
        const barColor = res.renewable ? 'var(--accent-success)' : 'var(--accent-warning)';

        const div = document.createElement('div');
        div.className = 'resource-item';
        div.innerHTML = `
            <div class="res-header">
                <span class="res-name"><i class="fa-solid ${iconClass}"></i> &nbsp; ${res.name}</span>
                <span class="res-values">${res.used} / ${res.total}</span>
            </div>
            <div class="progress-track">
                <div class="progress-bar" style="width: ${res.usage_percent}%; background-color: ${barColor}"></div>
            </div>
            <div class="progress-info">
                <span>Usage: ${res.usage_percent}%</span>
                <span style="color: ${res.renewable ? 'var(--accent-success)' : 'var(--text-muted)'}">
                    ${res.renewable ? 'Renewable' : 'Non-Renewable'}
                </span>
            </div>
        `;
        list.appendChild(div);
    });

    // Alerts
    const alertsArea = document.getElementById('alerts-area');
    alertsArea.innerHTML = '';

    if (metrics.alerts && metrics.alerts.length > 0) {
        // Update header badge
        const badge = document.getElementById('system-status');
        badge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Warning';
        badge.style.backgroundColor = 'rgba(239, 68, 68, 0.2)';
        badge.style.borderColor = 'var(--accent-danger)';
        badge.style.color = 'var(--accent-danger)';

        metrics.alerts.forEach(alertText => {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert';
            alertDiv.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> <span>${alertText}</span>`;
            alertsArea.appendChild(alertDiv);
        });
    }
}

function renderImpact(impact, metrics) {
    const container = document.getElementById('impact-content');
    const recArea = document.getElementById('recommendation-area');

    if (impact.status === 'simulated_internal') {
        container.innerHTML = `
            <div class="metric-big" style="text-align: center; padding: 1rem;">
                <h4 style="font-size: 3rem; margin: 0; color: var(--accent-danger);">${impact.total_co2e.toFixed(1)}</h4>
                <p style="margin: 0; color: var(--text-muted); font-size: 0.9rem;">${impact.unit}</p>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-muted); text-align: center; margin-top: 1rem;">
                ${impact.description}
            </p>
        `;
    }

    recArea.innerHTML = `
        <h4><i class="fa-solid fa-microchip"></i> AI Analysis</h4>
        <p style="margin-bottom: 0;">${metrics.recommendation}</p>
    `;
}
