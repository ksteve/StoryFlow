import { renderTimelines } from './renderTimeline.js';

document.addEventListener('DOMContentLoaded', async () => {
  const data = await fetch('./data/timelines.json').then(res => res.json());
  renderTimelines(data, document.getElementById('timeline-root'));
});
