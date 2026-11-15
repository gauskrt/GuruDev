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
    // 'Libs/projects/notable works/butterfly.jpg',
    // 'Libs/projects/notable works/car.jpg',
    // 'Libs/projects/notable works/chamelion.jpg',
    // 'Libs/projects/notable works/frogs.jpg',
    // 'Libs/projects/notable works/hosre.jpg',
    // 'Libs/projects/notable works/monkey.jpg',
    // 'Libs/projects/notable works/Mouse.jpg',
    // 'Libs/projects/notable works/mouse_in_shoe.jpg',
    // 'Libs/projects/notable works/on_bench.jpg',
    // 'Libs/projects/notable works/panda.jpg',
    // 'Libs/projects/notable works/sparta.jpg',
    // 'Libs/projects/notable works/spongbob.jpg',
    // 'Libs/projects/notable works/squirral.jpg',
    // 'Libs/projects/notable works/teddy_bear.jpg',
    // 'Libs/projects/notable works/the_pearl.jpg',
    // 'Libs/projects/notable works/tiger.jpg',
    'Libs/projects/projects/daily project/1.jpg',
    'Libs/projects/projects/daily project/2.jpg',
    'Libs/projects/projects/daily project/3.jpg',
    'Libs/projects/projects/daily project/4.jpg',
    'Libs/projects/projects/daily project/5.jpg',
    'Libs/projects/projects/daily project/6.jpg',
    'Libs/projects/projects/daily project/7.jpg',
    'Libs/projects/projects/daily project/8.jpg',
    'Libs/projects/projects/daily project/9.jpg',
    'Libs/projects/projects/daily project/10.jpg',
    'Libs/projects/projects/daily project/11.jpg',
    'Libs/projects/projects/daily project/12.jpg',
    'Libs/projects/projects/daily project/13.jpg',
    'Libs/projects/projects/daily project/14.jpg',
    'Libs/projects/projects/daily project/15.jpg',
    'Libs/projects/projects/daily project/16.jpg',
    'Libs/projects/projects/daily project/17.jpg',
    'Libs/projects/projects/daily project/18.jpg',
    'Libs/projects/projects/daily project/19.jpg',
    'Libs/projects/projects/daily project/20.jpg',
    'Libs/projects/projects/daily project/bat_monkey.jpg',
    'Libs/projects/projects/daily project/duck.jpg',
    'Libs/projects/projects/daily project/fire.jpg',
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
  const START_DATE = new Date('2021-12-24'); // ← This is my start date. The day when history started.

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
     6. SCROLL PROJECT — auto-scrolling panorama
     The image is cloned so it loops seamlessly.
     It auto-scrolls, and the user can also drag or
     wheel-scroll it; auto-scroll pauses briefly on
     interaction, then resumes.
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
  const spTrack = document.getElementById('spTrack');
  const spImg   = document.getElementById('spImg');
  const spInner = document.getElementById('spScrollInner');

  if (spTrack && spImg && spInner) {
    const clone = spImg.cloneNode(true);
    clone.removeAttribute('id');
    clone.setAttribute('aria-hidden', 'true');
    spTrack.appendChild(clone);

    let half = 0;
    const measure = () => { half = spTrack.scrollWidth / 2; };
    if (spImg.complete) measure(); else spImg.addEventListener('load', measure);
    window.addEventListener('resize', measure, { passive: true });

    const SPEED = 0.9;          // px per frame — increase for faster auto-scroll
    const RESUME_MS = 2000;     // idle time before auto-scroll resumes
    let paused = false;
    let resumeTimer;

    const pauseAuto = () => {
      paused = true;
      clearTimeout(resumeTimer);
      resumeTimer = setTimeout(() => { paused = false; }, RESUME_MS);
    };

    const loop = () => {
      if (half) {
        if (!paused) spInner.scrollLeft += SPEED;
        if (spInner.scrollLeft >= half) spInner.scrollLeft -= half;
      }
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);

    // Drag to pan
    let dragging = false, startX = 0, startScroll = 0;
    spInner.addEventListener('pointerdown', e => {
      dragging = true;
      startX = e.clientX;
      startScroll = spInner.scrollLeft;
      spInner.setPointerCapture(e.pointerId);
      spInner.classList.add('dragging');
      pauseAuto();
    });
    spInner.addEventListener('pointermove', e => {
      if (!dragging) return;
      spInner.scrollLeft = startScroll - (e.clientX - startX);
      pauseAuto();
    });
    const endDrag = () => {
      if (!dragging) return;
      dragging = false;
      spInner.classList.remove('dragging');
      pauseAuto();
    };
    spInner.addEventListener('pointerup', endDrag);
    spInner.addEventListener('pointercancel', endDrag);

    // Wheel to scroll horizontally
    spInner.addEventListener('wheel', e => {
      const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      if (delta) { spInner.scrollLeft += delta; pauseAuto(); }
    }, { passive: true });
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
  document.getElementById('lbCloseCircle')?.addEventListener('click', closeLb);
  lb?.addEventListener('click', e => { if (e.target === lb) closeLb(); });

  /* Carousel images + inspiration image → open in the lightbox */
  document.getElementById('img-carousels')?.addEventListener('click', e => {
    const img = e.target.closest('.ic-img');
    if (img?.naturalWidth) openLb(img.src, '');
  });
  const inspireClickImg = document.getElementById('inspireParallax');
  inspireClickImg?.addEventListener('click', () => {
    if (inspireClickImg.naturalWidth) openLb(inspireClickImg.src, '');
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeLb(); focusCard(null); }
  });

  /* ─────────────────────────────────────────────────────────────
     9. IN YOUR SPACE — "Try another piece" swaps the art in a room
        Lists are split by shape so the frames never change size.
     ───────────────────────────────────────────────────────────── */
  const NW = 'Libs/projects/notable works/';
  const DP = 'Libs/projects/projects/daily project/';
  const nw = (f, t) => [NW + f + '.jpg', t];
  const dp = (f, t) => [DP + f + '.jpg', t];

  /* Pieces each frame shape can cycle through. Add or rename freely. */
  const ROOM_ART = {
    square:   [nw('pebble_koi','Pebble Koi'), nw('three_monkeys','Three Monkeys'), nw('panda','Panda'), nw('the_pearl','The Pearl'), nw('butterfly','Butterfly'), nw('frogs','Frogs'),
               nw('on_bench','On the Bench'), nw('squirral','Squirrel'), nw('car','Car')],
    portrait: [nw('elephants','Mother & Calf'), nw('lion','Lion'), nw('betta','Betta'), nw('jellyfish','Jellyfish'),
               nw('sky_lanterns','Sky Lanterns'), nw('dog','Curious Pup'), nw('bluebird','Bluebird'), nw('dolphins','Dolphins'),
               nw('tiger','Tiger'), nw('chamelion','Chameleon'), nw('hosre','Horse'), nw('sparta','Sparta'),
               nw('teddy_bear','Teddy Bear'), nw('Mouse','Mouse'), nw('mouse_in_shoe','Mouse in a Shoe')],
    landscape: [nw('whale','Whale'), nw('astronaut','Astronaut'), nw('jaguar','Jaguar'), nw('zebra','Zebra'),
               nw('koi_swirl','Koi Swirl'), nw('road_home','Road Home'), nw('balloon','Hot Air Balloon')],
    /* Small works — daily sketchbook drawings, used for cards, kids' room and the collage.
       EDIT the titles to your own names for these pieces. */
    small:    [dp('4','Penguin'), dp('11','Blue Bear'), dp('1','Bunny & Turtle'), dp('10','Mara the Meerkat'),
               dp('5','Husky'), dp('15','Elephants'), dp('6','Saturn in Hand'), dp('duck','Duck at Dusk'),
               dp('16','The Pilot'), dp('7','Bread of Adam'), dp('14','Jackal God'), dp('3','Antlered Beast'),
               dp('19','Sun Stone'), dp('fire','Campfire'), dp('18','Robot Monk'), dp('8','Fruit-Hat Monkey'),
               dp('17','Flute Player'), dp('13','The Potter'), dp('9','Planet Express'), dp('2','First Steps'),
               dp('booster','Booster')]
  };
  const nameOf = src => decodeURIComponent(String(src)).split('/').slice(-2).join('/');
  const joinTitles = t => t.length === 1 ? t[0] : t.length === 2 ? t.join(' & ')
                         : t.slice(0, -1).join(', ') + ' & ' + t.slice(-1);

  /* Get the next pieces from a list, skipping ones already in use */
  function nextFrom(list, currentSrc, inUse) {
    const cur = list.findIndex(a => nameOf(a[0]) === nameOf(currentSrc));
    for (let k = 1; k <= list.length; k++) {
      const cand = list[(cur + k + list.length) % list.length];
      if (!inUse.includes(nameOf(cand[0]))) return cand;
    }
    return list[0];
  }

  function swapImg(el, src, title, attr, wrap) {
    wrap.classList.add('swapping');
    setTimeout(() => {
      if (attr) el.setAttribute(attr, encodeURI(src)); else el.src = src;
      if (el.tagName === 'IMG') el.alt = title + ' by GuruDev';
      setTimeout(() => wrap.classList.remove('swapping'), 120);
    }, 250);
  }

  document.querySelectorAll('.room-card').forEach(card => {
    const btn = card.querySelector('.room-swap');
    const titleEl = card.querySelector('.room-art-title');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const slots = [...card.querySelectorAll('[data-shape]')];
      const imgOf = s => s.querySelector('img, image');
      const srcOf = s => { const i = imgOf(s); return i.tagName === 'IMG' ? i.getAttribute('src') : i.getAttribute('href'); };
      const inUse = slots.map(s => nameOf(srcOf(s)));
      const titles = [];
      slots.forEach((slot, i) => {
        const list = ROOM_ART[slot.dataset.shape] || ROOM_ART.square;
        const [src, title] = nextFrom(list, srcOf(slot), inUse);
        inUse[i] = nameOf(src);
        titles.push(title);
        const im = imgOf(slot);
        swapImg(im, src, title, im.tagName === 'IMG' ? null : 'href', slot);
        // cards show the drawing's name instead of a signature
        if (slot.classList.contains('card-x')) setTimeout(() => { slot.dataset.title = title; }, 250);
        const nameEl = slot.parentNode && slot.parentNode.querySelector && slot.parentNode.querySelector('.card-name');
        if (nameEl) setTimeout(() => { nameEl.textContent = title; }, 250);
      });
      if (titleEl) titleEl.textContent = titles.length > 4 ? titles.length + ' small works' : joinTitles(titles);
    });
  });

  /* Collage wall — built from the small-works list. Slots are x, y, w, h in cqw,
     frame colour: b = black, o = oak, w = white. */
  const COLLAGE_SLOTS = [
    [12,10,8.5,11,'o'], [22,6,12,15,'b'], [35.5,4,16,12,'w'], [53,6,10,10,'b'], [64.5,3,13,17,'o'], [79,8,10,13,'b'],
    [12,22.5,8.5,9,'b'], [22,22.5,9,9,'w'], [32.5,17.5,10,13,'b'], [44,17.5,19,13,'o'], [64.5,21.5,13,10,'w'], [79,22.5,10,9,'o'],
    [33,32,12,10,'o'], [46.5,32,9,11,'b'], [57,32,13,9.5,'b']
  ];
  const collage = document.getElementById('collageWall');
  if (collage) {
    const start = 0;
    COLLAGE_SLOTS.forEach(([x, y, w, h, c], i) => {
      const [src, title] = ROOM_ART.small[(start + i) % ROOM_ART.small.length];
      const f = document.createElement('div');
      f.className = 'cframe cf-' + c;
      f.dataset.shape = 'small';
      f.style.cssText = `left:${x}cqw; top:${y}cqw; width:${w}cqw; height:${h}cqw;`;
      f.innerHTML = `<img src="${src}" alt="${title} by GuruDev" draggable="false" />`;
      collage.appendChild(f);
    });
  }

  /* ─────────────────────────────────────────────────────────────
     10. Light protection: no right-click "Save image" on artwork,
         plus a live year in the footer.
     ───────────────────────────────────────────────────────────── */
  document.addEventListener('contextmenu', e => {
    if (e.target.tagName === 'IMG') e.preventDefault();
  });
  document.querySelectorAll('img').forEach(i => i.setAttribute('draggable', 'false'));
  const yearNow = document.getElementById('yearNow');
  if (yearNow) yearNow.textContent = new Date().getFullYear();

});
