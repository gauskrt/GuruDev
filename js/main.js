/* ═══════════════════════════════════════════════════════════════
   GURUDEV PORTFOLIO — main.js

   SECTIONS IN THIS FILE
   ─────────────────────────────────────────────────────────────
   1. NAV           shrinks / frosts when you scroll down
   2. HERO CAROUSEL loops the 3 background images every 4.5 s
   3. SCROLL REVEAL fades elements in as they enter the viewport
   4. COUNTER       split-flap day counter
                      ↳ SET YOUR START DATE on the line below ↓
   5. PARALLAX      inspiration image drifts gently on scroll
   6. SCROLL PROJECT drag-to-pan the panoramic image
   7. PROJECT 52    duplicates items for the infinite loop strip
   8. NOTABLE WORKS pop-to-front click + lightbox
   ═══════════════════════════════════════════════════════════════ */

'use strict';

document.addEventListener('DOMContentLoaded', () => {

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     DARK MODE TOGGLE
     Persists choice in localStorage.
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) document.documentElement.setAttribute('data-theme', savedTheme);

  const dmToggle = document.getElementById('darkModeToggle');
  dmToggle?.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     EXHIBITIONS DROPDOWN
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const exDropdown = document.getElementById('exhibitionsDropdown');
  const exToggle   = exDropdown?.querySelector('.nav-dropdown-toggle');

  exToggle?.addEventListener('click', e => {
    e.stopPropagation();
    const isOpen = exDropdown.classList.toggle('open');
    exToggle.setAttribute('aria-expanded', String(isOpen));
  });
  document.addEventListener('click', () => {
    exDropdown?.classList.remove('open');
    exToggle?.setAttribute('aria-expanded', 'false');
  });

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     IMAGE CAROUSELS
     CAROUSEL_IMAGES — replace these paths with
     your own artwork once you drop images into
     images/Libs/carousel/
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const CAROUSEL_IMAGES = [
    'images/doodles/doodle-01.svg', 'images/doodles/doodle-02.svg',
    'images/doodles/doodle-03.svg', 'images/doodles/doodle-04.svg',
    'images/doodles/doodle-05.svg', 'images/doodles/doodle-06.svg',
    'images/doodles/doodle-07.svg', 'images/doodles/doodle-08.svg',
    'images/doodles/doodle-09.svg', 'images/doodles/doodle-10.svg',
    'images/doodles/doodle-11.svg', 'images/doodles/doodle-12.svg',
    'images/doodles/doodle-13.svg', 'images/doodles/doodle-14.svg',
    'images/doodles/doodle-15.svg', 'images/doodles/doodle-16.svg',
    'images/doodles/doodle-17.svg', 'images/doodles/doodle-18.svg',
    'images/doodles/doodle-19.svg', 'images/doodles/doodle-20.svg',
    'images/doodles/doodle-21.svg', 'images/doodles/doodle-22.svg',
  ];

  function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function buildCarousel(trackId, images) {
    const track = document.getElementById(trackId);
    if (!track) return;

    // Fill 50 slots, no adjacent duplicates
    const pool  = shuffle(images);
    const slots = [];
    while (slots.length < 50) {
      for (const src of shuffle(pool)) {
        if (slots[slots.length - 1] !== src) slots.push(src);
        if (slots.length >= 50) break;
      }
    }

    const frag = document.createDocumentFragment();
    slots.forEach(src => {
      const img = document.createElement('img');
      img.src = src; img.alt = ''; img.className = 'ic-img';
      img.onerror = function () {
        const ph = document.createElement('div');
        ph.className = 'ic-img-ph';
        this.parentNode?.replaceChild(ph, this);
      };
      frag.appendChild(img);
    });
    track.appendChild(frag);
    // Duplicate for seamless CSS loop
    Array.from(track.children).forEach(c => track.appendChild(c.cloneNode(true)));
  }

  buildCarousel('icTrack1', CAROUSEL_IMAGES);
  buildCarousel('icTrack2', shuffle(CAROUSEL_IMAGES));

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     1. NAV — frost + shrink on scroll
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     2. HERO CAROUSEL — cycles every 4.5 s
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const slides = document.querySelectorAll('.hc-slide');
  if (slides.length > 1) {
    let cur = 0;
    setInterval(() => {
      slides[cur].classList.remove('active');
      cur = (cur + 1) % slides.length;
      slides[cur].classList.add('active');
    }, 4500);
  }

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     3. SCROLL REVEAL
     Add  data-reveal="fade-up|fade-right|fade-left"
     and optionally  data-delay="200"  (ms) to any
     element in the HTML to make it animate in.
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const revealEls = document.querySelectorAll('[data-reveal]');
  revealEls.forEach(el => {
    el.style.transitionDelay = (parseInt(el.dataset.delay || '0', 10)) + 'ms';
  });

  const revObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in-view'); revObs.unobserve(e.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

  revealEls.forEach(el => revObs.observe(el));

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     4. SPLIT-FLAP DAY COUNTER
     ↓ EDIT THIS DATE — use the format YYYY-MM-DD
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const START_DATE = new Date('2022-01-06'); // ← This is my start date. The day when history started.

  class SplitFlapDigit {
    constructor(el) {
      el.innerHTML = `
        <div class="sf-upper"><span class="sf-n">0</span></div>
        <div class="sf-lower"><span class="sf-n">0</span></div>
        <div class="sf-card-top"><span class="sf-n">0</span></div>
        <div class="sf-card-bot"><span class="sf-n">0</span></div>
      `;
      this._uN    = el.querySelector('.sf-upper .sf-n');
      this._lN    = el.querySelector('.sf-lower .sf-n');
      this._cTop  = el.querySelector('.sf-card-top');
      this._cTopN = el.querySelector('.sf-card-top .sf-n');
      this._cBot  = el.querySelector('.sf-card-bot');
      this._cBotN = el.querySelector('.sf-card-bot .sf-n');
      this.value  = '0';
    }

    set(ch) {
      this.value = ch;
      this._uN.textContent = this._lN.textContent = this._cTopN.textContent = ch;
    }

    flip(ch) {
      if (ch === this.value) return Promise.resolve();
      return new Promise(resolve => {
        const old = this.value;
        this.value = ch;
        this._uN.textContent    = ch;
        this._cTopN.textContent = old;
        this._cBotN.textContent = ch;
        this._cTop.classList.remove('sf-flip');
        this._cBot.classList.remove('sf-reveal');
        void this._cTop.offsetWidth; // force reflow
        this._cTop.classList.add('sf-flip');
        this._cBot.classList.add('sf-reveal');
        setTimeout(() => {
          this._lN.textContent    = ch;
          this._cTopN.textContent = ch;
          this._cTop.classList.remove('sf-flip');
          this._cBot.classList.remove('sf-reveal');
          resolve();
        }, 380);
      });
    }
  }

  const counterEl = document.getElementById('dayCounter');
  if (counterEl) {
    const totalDays = Math.max(0, Math.floor((Date.now() - START_DATE) / 86400000));
    const numDigits = Math.max(3, String(totalDays).length);
    const target    = String(totalDays).padStart(numDigits, '0');

    counterEl.innerHTML = '';
    counterEl.className = 'sf-display';
    const digits = Array.from({ length: numDigits }, () => {
      const slot = document.createElement('div');
      slot.className = 'sf-digit';
      counterEl.appendChild(slot);
      return new SplitFlapDigit(slot);
    });

    const wait = ms => new Promise(r => setTimeout(r, ms));

    const runCounter = async () => {
      const scrambleEnd = Date.now() + 1400;
      while (Date.now() < scrambleEnd) {
        digits.forEach(d => d.set(String(Math.floor(Math.random() * 10))));
        await wait(70);
      }
      for (let i = 0; i < digits.length; i++) {
        await wait(120);
        await digits[i].flip(target[i]);
      }
    };

    const cObs = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) { runCounter(); cObs.disconnect(); }
    }, { threshold: 0.4 });
    cObs.observe(counterEl);
  }

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     5. PARALLAX — inspiration section image
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const inspireImg = document.getElementById('inspireParallax');
  const inspireSec = document.getElementById('inspiration');

  window.addEventListener('scroll', () => {
    if (!inspireImg || !inspireSec) return;
    const rect     = inspireSec.getBoundingClientRect();
    const progress = 1 - (rect.bottom / (window.innerHeight + rect.height));
    inspireImg.style.transform = `translateY(${(progress - 0.5) * 18}%)`;
  }, { passive: true });

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     6. SCROLL PROJECT — drag-to-pan
     Mouse drag and touch swipe both work.
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const spCinematic = document.getElementById('spCinematic');
  const spInner     = document.getElementById('spScrollInner');
  const spDragHint  = document.getElementById('spDragHint');

  if (spCinematic && spInner) {
    let isDragging = false, startX = 0, startSL = 0;

    spCinematic.addEventListener('mousedown', e => {
      isDragging = true; startX = e.pageX; startSL = spInner.scrollLeft;
    });
    document.addEventListener('mouseup', () => { isDragging = false; });
    spCinematic.addEventListener('mousemove', e => {
      if (!isDragging) return;
      e.preventDefault();
      spInner.scrollLeft = startSL - (e.pageX - startX) * 1.4;
    });

    let touchStartX = 0, touchSL = 0;
    spCinematic.addEventListener('touchstart', e => {
      touchStartX = e.touches[0].pageX; touchSL = spInner.scrollLeft;
    }, { passive: true });
    spCinematic.addEventListener('touchmove', e => {
      spInner.scrollLeft = touchSL - (e.touches[0].pageX - touchStartX);
    }, { passive: true });

    if (spDragHint) {
      spInner.addEventListener('scroll', () => spDragHint.classList.add('hidden'), { once: true });
    }
  }

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     7. PROJECT 52 — infinite looping strip
     Clones all items so the CSS translateX(-50%)
     animation loops seamlessly.
     Speed is set by the `speed` variable (px/s).
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const p52Strip = document.getElementById('p52Strip');
  if (p52Strip) {
    Array.from(p52Strip.children).forEach(item => {
      const clone = item.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      p52Strip.appendChild(clone);
    });
    const speed = 80; // pixels per second — increase for faster scroll
    p52Strip.style.animationDuration = (p52Strip.scrollWidth / 2 / speed) + 's';
  }

  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     8. NOTABLE WORKS — pop-to-front + lightbox
     • Hover  → siblings dim
     • 1st click → focused card scales forward
     • 2nd click on focused → full-screen lightbox
     • Click outside grid or press ESC → resets
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const lb      = document.getElementById('lightbox');
  const lbImg   = document.getElementById('lbImg');
  const lbCap   = document.getElementById('lbCap');
  const lbClose = document.getElementById('lbClose');
  const nwGrid  = document.querySelector('.nw-grid');

  const openLb = (src, caption) => {
    if (!lb) return;
    lbImg.src = src;
    lbCap.textContent = caption || '';
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  };
  const closeLb = () => {
    if (!lb) return;
    lb.classList.remove('open');
    document.body.style.overflow = '';
    setTimeout(() => { lbImg.src = ''; }, 400);
  };
  const focusCard = card => {
    document.querySelectorAll('.nw-card.nw-focused').forEach(c => c.classList.remove('nw-focused'));
    nwGrid?.classList.remove('has-focused');
    if (card) { card.classList.add('nw-focused'); nwGrid?.classList.add('has-focused'); }
  };

  document.querySelectorAll('.nw-card').forEach(card => {
    card.addEventListener('click', e => {
      e.stopPropagation();
      if (card.classList.contains('nw-focused')) {
        const img = card.querySelector('img');
        if (img?.naturalWidth) openLb(img.src, card.querySelector('.nw-title')?.textContent);
      } else {
        focusCard(card);
      }
    });
  });

  document.addEventListener('click', e => { if (!e.target.closest('.nw-grid')) focusCard(null); });
  lbClose?.addEventListener('click', closeLb);
  lb?.addEventListener('click', e => { if (e.target === lb) closeLb(); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeLb(); focusCard(null); }
  });

});
