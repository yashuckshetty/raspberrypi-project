// ================= THINGSPEAK DETAILS =================
const CHANNEL_ID = "3243397";
const READ_API_KEY = "DXSXNX6M7V3ZQX7T";

const API_URL = `https://api.thingspeak.com/channels/${CHANNEL_ID}/feeds.json?api_key=${READ_API_KEY}&results=20`;

let runChart, idleChart, utilChart;

async function loadData() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        const feeds = data.feeds;

        // FILTER ONLY VALID DATA
        const validFeeds = feeds.filter(f =>
            f.field1 !== "120" &&
            f.field2 !== "45" &&
            f.field3 !== "72"
        );

        const labels = validFeeds.map(f => f.created_at.slice(11, 19));
        const runData = validFeeds.map(f => parseFloat(f.field1));
        const idleData = validFeeds.map(f => parseFloat(f.field2));
        const utilData = validFeeds.map(f => parseFloat(f.field3));

        updateRunChart(labels, runData);
        updateIdleChart(labels, idleData);
        updateUtilChart(labels, utilData);

    } catch (err) {
        console.error("Data fetch error:", err);
    }
}

// ================= RUN CHART =================
function updateRunChart(labels, data) {
    if (!runChart) {
        runChart = new Chart(document.getElementById("runChart"), {
            type: "line",
            data: {
                labels,
                datasets: [{
                    label: "Running Time (sec)",
                    data,
                    borderColor: "green",
                    tension: 0.4
                }]
            },
            options: { responsive: true }
        });
    } else {
        runChart.data.labels = labels;
        runChart.data.datasets[0].data = data;
        runChart.update();
    }
}

// ================= IDLE CHART =================
function updateIdleChart(labels, data) {
    if (!idleChart) {
        idleChart = new Chart(document.getElementById("idleChart"), {
            type: "line",
            data: {
                labels,
                datasets: [{
                    label: "Idle Time (sec)",
                    data,
                    borderColor: "orange",
                    tension: 0.4
                }]
            },
            options: { responsive: true }
        });
    } else {
        idleChart.data.labels = labels;
        idleChart.data.datasets[0].data = data;
        idleChart.update();
    }
}

// ================= UTILIZATION CHART =================
function updateUtilChart(labels, data) {
    if (!utilChart) {
        utilChart = new Chart(document.getElementById("utilChart"), {
            type: "line",
            data: {
                labels,
                datasets: [{
                    label: "Utilization (%)",
                    data,
                    borderColor: "blue",
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { min: 0, max: 100 }
                }
            }
        });
    } else {
        utilChart.data.labels = labels;
        utilChart.data.datasets[0].data = data;
        utilChart.update();
    }
}

// ================= AUTO REFRESH =================
loadData();
setInterval(loadData, 15000);
