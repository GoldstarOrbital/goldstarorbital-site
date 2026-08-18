// Goldstar Orbital — site interactivity
// Mobile nav, scroll-reveal, phase tabs, compression demo, video filter, active-link tracking.

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Starfield background (subtle, hero-only) ---------- */
  (function starfield() {
    const root = document.getElementById('starfield');
    if (!root) return;
    function makeLayer(count, sizeRange, className) {
      const layer = document.createElement('div');
      layer.className = 'layer ' + className;
      const w = root.parentElement.offsetWidth + 100, h = root.parentElement.offsetHeight + 100;
      let shadows = [];
      for (let i = 0; i < count; i++) {
        const x = Math.floor(Math.random() * w);
        const y = Math.floor(Math.random() * h);
        const s = (Math.random() * (sizeRange[1] - sizeRange[0]) + sizeRange[0]).toFixed(1);
        shadows.push(`${x}px ${y}px 0 ${s}px rgba(232,230,223,${(Math.random()*0.4+0.2).toFixed(2)})`);
      }
      layer.style.width = '2px';
      layer.style.height = '2px';
      layer.style.boxShadow = shadows.join(',');
      layer.style.background = 'transparent';
      root.appendChild(layer);
    }
    makeLayer(36, [0, 0.5], 'layer-1');
    makeLayer(20, [0, 0.35], 'layer-2');
  })();

  /* ---------- Mobile nav toggle ---------- */
  const toggle = document.querySelector('.navtoggle');
  const links = document.querySelector('.navlinks');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const open = links.style.display === 'flex';
      links.style.display = open ? 'none' : 'flex';
      links.style.flexDirection = 'column';
      links.style.position = 'absolute';
      links.style.top = '64px';
      links.style.left = '0';
      links.style.right = '0';
      links.style.background = '#0e131b';
      links.style.padding = '20px 28px';
      links.style.borderBottom = '1px solid #232b3a';
      toggle.setAttribute('aria-expanded', String(!open));
    });
  }

  /* ---------- Active nav link on scroll ---------- */
  const sections = document.querySelectorAll('main section[id]');
  const navAnchors = document.querySelectorAll('.navlinks a');
  const setActive = () => {
    let current = '';
    sections.forEach(sec => {
      const rect = sec.getBoundingClientRect();
      if (rect.top <= 120 && rect.bottom >= 120) current = sec.id;
    });
    navAnchors.forEach(a => {
      a.style.color = a.getAttribute('href') === `#${current}` ? '#f4b731' : '';
    });
  };
  document.addEventListener('scroll', setActive, { passive: true });
  setActive();

  /* ---------- Scroll reveal ---------- */
  const revealTargets = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealTargets.forEach(el => io.observe(el));
  } else {
    revealTargets.forEach(el => el.classList.add('is-visible'));
  }

  /* ---------- Roadmap phase tabs ---------- */
  const phaseButtons = document.querySelectorAll('.phase-btn');
  const phasePanels = document.querySelectorAll('.phase-panel');
  phaseButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.phase;
      phaseButtons.forEach(b => b.classList.toggle('active', b === btn));
      phasePanels.forEach(p => p.classList.toggle('active', p.dataset.phase === target));
    });
  });

  /* ---------- Technical deep-dive toggle ---------- */
  const deepdiveToggle = document.getElementById('deepdive-toggle');
  const deepdiveContent = document.getElementById('deepdive-content');
  if (deepdiveToggle && deepdiveContent) {
    deepdiveToggle.addEventListener('click', () => {
      const open = deepdiveToggle.getAttribute('aria-expanded') === 'true';
      deepdiveToggle.setAttribute('aria-expanded', String(!open));
      deepdiveContent.hidden = open;
      if (!open) {
        deepdiveContent.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-visible'));
      }
    });
  }

  /* ---------- Expandable feature cards (Fawn / Functioning Faith) ---------- */
  document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('click', () => {
      const open = card.getAttribute('aria-expanded') === 'true';
      card.setAttribute('aria-expanded', String(!open));
    });
  });

  /* ---------- Mission architecture figure gallery ---------- */
  const FIGURES = [
    { file: 'fig1-controller-passive-node.png', title: 'FIG. 1 — Controller Satellite & Passive Node', desc: 'RTG power, photonic GPU core, quantum memory, and the 4-beam interface between them.' },
    { file: 'fig0-satellite-lab.png', title: 'FIG. 0 — Original Photonic-Lab Concept', desc: 'The May 2026 original concept: photonic payload, solar arrays, optical link to ground.' },
    { file: 'fig2-node-datasheet.png', title: 'FIG. 2 — Satellite Node Architecture', desc: 'RTG power, photonic GPU mesh, quantum memory, encoding table, photosynthesis delivery.' },
    { file: 'fig3-orbital-constellation.png', title: 'FIG. 3 — Orbital Constellation', desc: 'Controller satellites and storage nodes around a planetary body, with delivery beam to a surface reactor.' },
    { file: 'fig4-dataflow.png', title: 'FIG. 4 — Data Flow', desc: 'Encoding, circulating storage, quantum freeze, decode, and the photosynthesis feedback loop.' },
    { file: 'fig5-multisymbol-rtg.png', title: 'FIG. 5 — Multi-Symbol Alphabet & RTG Power', desc: 'The encoding alphabet, wavelength reference, and RTG power decay curve versus solar.' },
    { file: 'fig6-security-photosynthesis.png', title: 'FIG. 6 — Security, Photosynthesis & Competitive Landscape', desc: 'Security architecture, photosynthesis blueprint, and the GPU comparison table.' }
  ];
  let galleryIndex = 0;
  const galleryImage = document.getElementById('gallery-image');
  const galleryTitle = document.getElementById('gallery-title');
  const galleryDesc = document.getElementById('gallery-desc');
  const galleryCounter = document.getElementById('gallery-counter');
  const galleryThumbs = document.getElementById('gallery-thumbs');

  function renderGallery() {
    if (!galleryImage) return;
    const fig = FIGURES[galleryIndex];
    galleryImage.src = 'assets/schematics/' + fig.file;
    galleryImage.alt = fig.title;
    galleryTitle.textContent = fig.title;
    galleryDesc.textContent = fig.desc;
    galleryCounter.textContent = (galleryIndex + 1) + ' / ' + FIGURES.length;
    galleryThumbs.querySelectorAll('button').forEach((b, i) => b.classList.toggle('active', i === galleryIndex));
  }
  if (galleryThumbs) {
    FIGURES.forEach((fig, i) => {
      const b = document.createElement('button');
      b.innerHTML = `<img src="assets/schematics/${fig.file}" alt="${fig.title}" loading="lazy">`;
      b.addEventListener('click', () => { galleryIndex = i; renderGallery(); });
      galleryThumbs.appendChild(b);
    });
    document.getElementById('gallery-prev').addEventListener('click', () => {
      galleryIndex = (galleryIndex - 1 + FIGURES.length) % FIGURES.length;
      renderGallery();
    });
    document.getElementById('gallery-next').addEventListener('click', () => {
      galleryIndex = (galleryIndex + 1) % FIGURES.length;
      renderGallery();
    });
    renderGallery();
  }

  /* ---------- Compression ratio demo ---------- */
  const ratioData = {
    zip:  { standard: 1.00, goldstar: 9.90, label: 'ZIP archive' },
    pdf:  { standard: 1.41, goldstar: 10.65, label: 'PDF document' },
    jpeg: { standard: 1.20, goldstar: 6.15, label: 'JPEG image' },
    docx: { standard: 3.35, goldstar: 6.19, label: 'Word document' }
  };
  const demoButtons = document.querySelectorAll('.ratio-btn');
  const barGoldstar = document.getElementById('bar-goldstar');
  const barStandard = document.getElementById('bar-standard');
  const readoutGoldstar = document.getElementById('readout-goldstar');
  const readoutStandard = document.getElementById('readout-standard');
  const readoutLabel = document.getElementById('readout-label');
  const readoutAdvantage = document.getElementById('readout-advantage');

  function animateRatio(key) {
    const d = ratioData[key];
    if (!d || !barGoldstar) return;
    const maxScale = 11; // chart ceiling
    barGoldstar.style.width = (d.goldstar / maxScale * 100) + '%';
    barStandard.style.width = (d.standard / maxScale * 100) + '%';
    readoutGoldstar.textContent = d.goldstar.toFixed(2) + 'x';
    readoutStandard.textContent = d.standard.toFixed(2) + 'x';
    readoutLabel.textContent = d.label;
    readoutAdvantage.textContent = (d.goldstar / d.standard).toFixed(2) + 'x better than standard tools';
  }
  demoButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      demoButtons.forEach(b => b.classList.toggle('active', b === btn));
      animateRatio(btn.dataset.filetype);
    });
  });
  if (demoButtons.length) animateRatio(demoButtons[0].dataset.filetype);

  /* ---------- Video portfolio filter ---------- */
  const filterButtons = document.querySelectorAll('.filter-btn');
  const videoCards = document.querySelectorAll('.video-card');
  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      filterButtons.forEach(b => b.classList.toggle('active', b === btn));
      const cat = btn.dataset.filter;
      videoCards.forEach(card => {
        const show = cat === 'all' || card.dataset.category === cat;
        card.style.display = show ? '' : 'none';
      });
    });
  });

  /* ---------- Click-to-play video facades (fast initial load, real interaction) ---------- */
  document.querySelectorAll('.video-frame-wrap[data-video-id]').forEach(wrap => {
    const id = wrap.dataset.videoId;
    const title = wrap.dataset.title || 'Video';
    const thumb = document.createElement('img');
    thumb.src = `https://i.ytimg.com/vi/${id}/hqdefault.jpg`;
    thumb.alt = title;
    thumb.loading = 'lazy';
    thumb.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;';
    const playBtn = document.createElement('button');
    playBtn.setAttribute('aria-label', 'Play ' + title);
    playBtn.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border:0;background:rgba(10,14,20,0.15);cursor:pointer;display:flex;align-items:center;justify-content:center;';
    playBtn.innerHTML = '<span style="width:56px;height:56px;border-radius:50%;background:rgba(244,183,49,0.92);display:flex;align-items:center;justify-content:center;font-size:20px;color:#14100a;transition:transform .15s ease;">▶</span>';
    playBtn.addEventListener('mouseenter', () => { playBtn.querySelector('span').style.transform = 'scale(1.08)'; });
    playBtn.addEventListener('mouseleave', () => { playBtn.querySelector('span').style.transform = 'none'; });
    playBtn.addEventListener('click', () => {
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube.com/embed/${id}?autoplay=1`;
      iframe.title = title;
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      iframe.allowFullscreen = true;
      iframe.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border:0;';
      wrap.innerHTML = '';
      wrap.appendChild(iframe);
    }, { once: true });
    wrap.appendChild(thumb);
    wrap.appendChild(playBtn);
  });

  /* ---------- Live clock in footer (small live element, low-key) ---------- */
  const clockEl = document.getElementById('utc-clock');
  if (clockEl) {
    const tick = () => {
      const now = new Date();
      clockEl.textContent = now.toUTCString().slice(17, 25) + ' UTC';
    };
    tick();
    setInterval(tick, 1000);
  }
});
