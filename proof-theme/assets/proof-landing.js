// ════════════════════════════════════════════════════════
// PROOF Display V17 — Main JavaScript
// All DOM queries wrapped in DOMContentLoaded/load guards
// Pilot form code removed (pilot section removed from page)
// ════════════════════════════════════════════════════════

// ── PRODUCT URL (from Liquid data-product-url) ──
function getProductUrl() {
  const root = document.getElementById('proof-landing');
  return (root && root.dataset.productUrl) || '#';
}

// ── SIMULATOR ──
function calcSim() {
  const curEl = document.getElementById('cur-reviews');
  const dailyEl = document.getElementById('daily-cust');
  const ratingEl = document.getElementById('cur-rating');
  const bizNameEl = document.getElementById('biz-name');
  const resultsEl = document.getElementById('sim-results');
  const noteEl = document.getElementById('sim-note');
  const ctaEl = document.getElementById('sim-cta');
  const ctaSubEl = document.getElementById('sim-cta-sub');

  if (!curEl || !dailyEl || !ratingEl || !resultsEl) return;

  const cur = parseInt(curEl.value) || 0;
  const daily = parseInt(dailyEl.value) || 0;
  const rating = parseFloat(ratingEl.value) || 4.0;
  const bizName = bizNameEl && bizNameEl.value.trim() ? bizNameEl.value.trim() : null;
  const bizLabel = bizName ? `For ${bizName}` : 'Your projection';

  const baseMonthly = Math.round(daily * 30 * 0.003);
  const proofMonthly = Math.round(daily * 30 * 0.007);
  const after6mo = cur + (proofMonthly * 6);
  const newRating = Math.min(5.0, rating + 0.15).toFixed(1);
  const extraReviews = after6mo - cur;

  resultsEl.innerHTML = `
    <div class="src"><div class="src-lbl">Without PROOF</div><div class="src-val">${baseMonthly}</div><div class="src-sub">reviews / month (est.)</div></div>
    <div class="src hi"><div class="src-lbl">With PROOF</div><div class="src-val">${proofMonthly}</div><div class="src-sub">reviews / month (est.)</div></div>
    <div class="src"><div class="src-lbl">6 months from now</div><div class="src-val">${after6mo}</div><div class="src-sub">${rating}★ → ${newRating}★ projected</div></div>
  `;

  if (noteEl) {
    const productUrl = getProductUrl();
    const personalised = bizName
      ? `${bizLabel}: <strong style="color:var(--white)">+${extraReviews} more reviews</strong> in 6 months. That's ${after6mo} total — enough to rank significantly higher on Google Maps. <a href="${productUrl}">Order now →</a>`
      : `That's <strong style="color:var(--white)">+${extraReviews} more reviews</strong> in 6 months — compounding your Google Maps ranking every week. <a href="${productUrl}">Order now to start →</a>`;
    noteEl.innerHTML = personalised;
  }

  if (ctaEl && ctaSubEl) {
    ctaEl.classList.add('show');
    const ctaText = bizName
      ? `${bizName} with ${after6mo} reviews and ${newRating}★ — that's a significantly stronger Google Maps presence. The counter is already there. Now it shows your reputation.`
      : `${extraReviews} more reviews means a stronger Maps ranking, more trust in your space, and more first-time visitors who already trust you before they walk in.`;
    ctaSubEl.textContent = ctaText;
  }
}

// ── STICKY BUY BAR ──
function initStickyBar() {
  const stickyBar = document.getElementById('sticky-bar');
  const heroEl = document.querySelector('.hero');

  if (!stickyBar || !heroEl) return;

  let heroBottom = 0;

  function updateHeroBottom() {
    heroBottom = heroEl.getBoundingClientRect().bottom + window.scrollY;
  }

  // Wait for layout to settle before measuring
  requestAnimationFrame(() => {
    updateHeroBottom();
  });

  window.addEventListener('resize', updateHeroBottom, { passive: true });
  window.addEventListener('scroll', () => {
    if (window.scrollY > heroBottom - window.innerHeight) {
      stickyBar.classList.add('visible');
    } else {
      stickyBar.classList.remove('visible');
    }
  }, { passive: true });
}

// ── NAV SCROLLED STATE ──
// Announcement bar removed in V17 — nav sits at top:0 always
function initNav() {
  const nav = document.getElementById('nav');
  if (!nav) return;

  // Nav is always at top:0 (no announcement bar)
  nav.style.top = '0px';

  window.addEventListener('scroll', () => {
    if (window.scrollY > 60) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  }, { passive: true });
}

// ── SCROLL REVEAL ──
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -32px 0px' });

  document.querySelectorAll('.reveal, .reveal-stagger').forEach(el => {
    observer.observe(el);
  });
}

// ── FAQ ACCORDION ──
function initFaq() {
  function toggleFaq(item) {
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => {
      i.classList.remove('open');
      i.setAttribute('aria-expanded', 'false');
    });
    if (!isOpen) {
      item.classList.add('open');
      item.setAttribute('aria-expanded', 'true');
    }
  }

  document.querySelectorAll('.faq-item').forEach(item => {
    item.addEventListener('click', () => toggleFaq(item));
    item.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleFaq(item);
      }
    });
  });
}

// ── VERTICAL CARDS ──
function initVertCards() {
  document.querySelectorAll('.vert-card').forEach(card => {
    card.addEventListener('click', () => {
      document.querySelectorAll('.vert-card').forEach(c => c.classList.remove('active'));
      card.classList.add('active');
    });
  });
}

// ── SIMULATOR INPUT LISTENERS ──
function initSimulatorInputs() {
  ['cur-reviews', 'daily-cust', 'cur-rating'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', calcSim);
  });
}

// ── EMBED RAIL: mark slots when global app widgets are present ──
function initEmbedRail() {
  const chatSlot = document.querySelector('.proof-embed-slot--chat');
  const salesSlot = document.querySelector('.proof-embed-slot--sales');
  if (!chatSlot && !salesSlot) return;

  function markActive() {
    const hasChat =
      document.getElementById('ShopifyChat') ||
      document.querySelector('[id*="ShopifyChat"], [class*="inbox"], iframe[title*="chat" i]');
    const hasSales = document.querySelector(
      '[class*="sales-pop"], [id*="sales-pop"], [class*="SalesPop"], [data-sales-pop]'
    );

    if (chatSlot) chatSlot.classList.toggle('is-active', !!hasChat);
    if (salesSlot) salesSlot.classList.toggle('is-active', !!hasSales);
  }

  markActive();
  const observer = new MutationObserver(markActive);
  observer.observe(document.body, { childList: true, subtree: true });
  window.setTimeout(markActive, 2000);
  window.setTimeout(markActive, 5000);
}

// ── BOOT: Run everything after DOM is ready ──
document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initFaq();
  initVertCards();
  initSimulatorInputs();
  initEmbedRail();
  calcSim(); // initial render
});

// Sticky bar needs layout measurements — run after full load
window.addEventListener('load', () => {
  initStickyBar();
  initScrollReveal();
});