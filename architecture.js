'use strict';
const drawings = [...document.querySelectorAll('.drawing')];
const selectors = [...document.querySelectorAll('[data-figure]')];
let currentFigure = 0;
function showFigure(index) {
  currentFigure = (index + drawings.length) % drawings.length;
  drawings.forEach((drawing, i) => { drawing.hidden = i !== currentFigure; });
  selectors.forEach((button, i) => button.setAttribute('aria-pressed', String(i === currentFigure)));
  document.getElementById('figure-count').textContent = `${currentFigure + 1} / ${drawings.length}`;
}
if (drawings.length) {
  selectors.forEach(button => button.addEventListener('click', () => showFigure(Number(button.dataset.figure))));
  document.getElementById('previous-figure').addEventListener('click', () => showFigure(currentFigure - 1));
  document.getElementById('next-figure').addEventListener('click', () => showFigure(currentFigure + 1));
  document.getElementById('figure-buttons').hidden = false;
  document.getElementById('gallery-controls').hidden = false;
  showFigure(0);
}
