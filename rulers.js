// Ornamental, unnumbered inch ticks scale with the paper width.
const horizontal = document.querySelector('.top-ruler');
const papers = [...document.querySelectorAll('.paper')];
function alignLeftRulers() {
  for (const paper of papers) {
    paper.previousElementSibling.style.left = `${8 - paper.getBoundingClientRect().left}px`;
  }
}
window.addEventListener('resize', alignLeftRulers);
const tick = (x1, y1, x2, y2) => `<path d="M${x1} ${y1}L${x2} ${y2}"/>`;
const knob = (x, right = false) => `<g transform="translate(${x} 0)" fill="#ffffff" stroke="#858b8e" stroke-width="1.2"><path d="M-6 0H6V5L0 12L-6 5Z"/>${right ? '' : '<path d="M0 13L6 19V24H-6V19Z"/><path d="M-6 24H6V29H-6Z"/>'}</g>`;
function drawHorizontal(width) {
  const unit = width / 8.5;
  let marks = '';
  for (let i = 0; i <= 68; i++) {
    const x = i * unit / 8;
    const major = i % 8 === 0;
    marks += tick(x, 11, x, major ? 23 : i % 4 === 0 ? 19 : 15);
  }
  horizontal.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="30" viewBox="0 0 ${width} 30" focusable="false"><path fill="#d7d8d5" d="M0 6H${width}V25H0Z"/><path fill="#ffffff" d="M${unit} 6H${width - unit}V25H${unit}Z"/><g stroke="#858b8e" stroke-width="1" fill="#62686d" >${marks}</g>${knob(unit)}${knob(width - unit, true)}</svg>`;
}
const observer = new ResizeObserver(entries => {
  alignLeftRulers();
  for (const {target} of entries) {
    const {width, height} = target.getBoundingClientRect();
    const unit = width / 8.5;
    if (target === papers[0]) drawHorizontal(width);
    let lines = '';
    for (let i = 0; i * unit / 8 < height; i++) {
      const y = i * unit / 8;
      lines += tick(i % 8 === 0 ? 5 : i % 4 === 0 ? 11 : 15, y, 20, y);
    }
    target.previousElementSibling.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="${height}" focusable="false"><path fill="#d7d8d5" d="M0 0H22V${height}H0Z"/><path fill="#ffffff" d="M0 ${unit}H22V${height - unit}H0Z"/><g stroke="#858b8e" stroke-width=".7" fill="#62686d" >${lines}</g></svg>`;
  }
});
papers.forEach(paper => observer.observe(paper));
