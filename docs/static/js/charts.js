function getPublicationTimelineData() {
    const counts = new Map();
    const publications = document.querySelectorAll('.publications-shell .reference-item');

    publications.forEach((publication) => {
        const meta = publication.querySelector('.publication-meta')?.textContent || '';
        const yearMatch = meta.match(/\b(19|20)\d{2}\b/);
        if (!yearMatch) return;

        const year = yearMatch[0];
        const section = publication.closest('ul')?.previousElementSibling?.textContent || '';
        const type = section.includes('Journal')
            ? 'journal'
            : section.includes('Conference papers')
                ? 'conference'
                : null;
        if (!type) return;
        const current = counts.get(year) || { conference: 0, journal: 0 };
        current[type] += 1;
        counts.set(year, current);
    });

    const labels = Array.from(counts.keys()).sort((a, b) => Number(a) - Number(b));
    return {
        labels,
        conference: labels.map((year) => counts.get(year).conference),
        journal: labels.map((year) => counts.get(year).journal),
    };
}

window.updatePublicationTimeline = function updatePublicationTimeline() {
    const canvas = document.getElementById('myStackedChart');
    if (!canvas || typeof Chart === 'undefined') return;

    const timeline = getPublicationTimelineData();
    if (!timeline.labels.length) return;

    if (canvas.__publicationTimeline) {
        canvas.__publicationTimeline.destroy();
    }

    const ctx = canvas.getContext('2d');
    canvas.__publicationTimeline = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: timeline.labels,
            datasets: [
                {
                    label: 'Conference Papers',
                    data: timeline.conference,
                    backgroundColor: 'rgba(30, 144, 255, 0.7)',
                },
                {
                    label: 'Journal Articles',
                    data: timeline.journal,
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
                x: { stacked: true },
                y: { stacked: true, beginAtZero: true, ticks: { precision: 0 } }
            }
        }
    });
};

function initializeChart() {
    window.updatePublicationTimeline();
}
