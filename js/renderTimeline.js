export function renderTimelines(timelines, container) {
  timelines.forEach(timeline => {
    const timelineDiv = document.createElement('div');
    timelineDiv.className = 'timeline';

    timeline.events.forEach(event => {
      const item = document.createElement('div');
      item.className = 'timeline-item';

      item.innerHTML = `
        <div class="dot"></div>
        <div class="content">
          <h3>${formatDate(event.date)}</h3>
          <p>${event.summary}</p>
        </div>
      `;

      timelineDiv.appendChild(item);
    });

    container.appendChild(timelineDiv);
  });
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
}
