const embedUrl = id => `https://drive.google.com/file/d/${id}/preview`;
const dlUrl    = id => `https://drive.google.com/uc?export=download&id=${id}`;

const treeEl   = document.getElementById('tree');
const frameEl  = document.getElementById('pdf-frame');
const titleEl  = document.getElementById('paper-title');
const dlBtn    = document.getElementById('dl-btn');
const searchEl = document.getElementById('search');

let DATA = {};

function paperLabel(year, session, p) {
  return `${year} ${session} — ${p.d} Shift ${p.s}`;
}

function render(filter = '') {
  const q = filter.trim().toLowerCase();
  treeEl.innerHTML = '';

  Object.keys(DATA).sort((a, b) => b - a).forEach(year => {
    const yearDetails = document.createElement('details');
    yearDetails.open = !!q; // auto-expand when searching

    const yearSummary = document.createElement('summary');
    yearSummary.textContent = year;
    yearDetails.appendChild(yearSummary);

    Object.entries(DATA[year]).forEach(([session, papers]) => {
      const matching = papers.filter(p =>
        !q || `${year} ${session} ${p.d} shift ${p.s}`.toLowerCase().includes(q)
      );
      if (!matching.length) return;

      const sessDetails = document.createElement('details');
      sessDetails.open = !!q;

      const sessSummary = document.createElement('summary');
      sessSummary.textContent = session;
      sessDetails.appendChild(sessSummary);

      matching.forEach(p => {
        const btn = document.createElement('button');
        btn.className = 'paper-btn';
        btn.textContent = `${p.d} · Shift ${p.s}`;
        btn.addEventListener('click', () => loadPaper(year, session, p));
        sessDetails.appendChild(btn);
      });

      yearDetails.appendChild(sessDetails);
    });

    if (yearDetails.querySelector('.paper-btn')) treeEl.appendChild(yearDetails);
  });
}

function loadPaper(year, session, p) {
  titleEl.textContent = paperLabel(year, session, p);
  frameEl.src        = embedUrl(p.i);
  dlBtn.href         = dlUrl(p.i);
  dlBtn.hidden       = false;

  // reflect in URL so it's shareable / bookmarkable
  const url = new URL(location);
  url.searchParams.set('id', p.i);
  history.replaceState(null, '', url);
}

searchEl.addEventListener('input', e => render(e.target.value));

fetch('/data/papers.json')
  .then(r => r.json())
  .then(json => {
    DATA = json;
    render();

    // deep-link support: /viewer/?id=FILE_ID
    const id = new URLSearchParams(location.search).get('id');
    if (id) {
      outer: for (const [year, sessions] of Object.entries(DATA))
        for (const [session, papers] of Object.entries(sessions))
          for (const p of papers)
            if (p.i === id) { loadPaper(year, session, p); break outer; }
    }
  })
  .catch(err => {
    console.error(err);
    treeEl.innerHTML = '<p class="error">Failed to load papers.json</p>';
  });
