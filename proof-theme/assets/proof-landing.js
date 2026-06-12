// PROOF Display V40 — landing interactions

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isDesignMode = typeof Shopify !== 'undefined' && Shopify.designMode;

  let lenis = null;

  function initLenis() {
    if (prefersReducedMotion || isDesignMode || typeof Lenis === 'undefined') return;

    lenis = new Lenis({
      duration: 1.4,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      smoothWheel: true,
    });

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
  }

  function initNavScroll() {
    const nav = document.getElementById('main-nav');
    if (!nav) return;

    window.addEventListener(
      'scroll',
      () => {
        nav.classList.toggle('scrolled', window.scrollY > 60);
      },
      { passive: true }
    );

    nav.querySelectorAll('a[href^="#"]').forEach((link) => {
      link.addEventListener('click', (e) => {
        const id = link.getAttribute('href');
        if (!id || id === '#') return;
        const target = document.querySelector(id);
        if (!target) return;
        e.preventDefault();
        if (lenis) {
          lenis.scrollTo(target, { offset: -80 });
        } else {
          target.scrollIntoView({ behavior: prefersReducedMotion ? 'auto' : 'smooth' });
        }
      });
    });
  }

  function initDeviceTilt() {
    if (prefersReducedMotion) return;
    const deviceScene = document.getElementById('deviceScene');
    const device3d = document.getElementById('device3d');
    if (!deviceScene || !device3d) return;

    deviceScene.addEventListener('mousemove', (e) => {
      const rect = deviceScene.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = (e.clientX - cx) / (rect.width / 2);
      const dy = (e.clientY - cy) / (rect.height / 2);
      device3d.style.transform = `rotateX(${8 - dy * 6}deg) rotateY(${-6 + dx * 8}deg)`;
    });

    deviceScene.addEventListener('mouseleave', () => {
      device3d.style.transform = 'rotateX(8deg) rotateY(-6deg)';
    });
  }

  function initScrollReveal() {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );

    document.querySelectorAll('.reveal, .reveal-stagger').forEach((el) => observer.observe(el));
  }

  function initQrStagger() {
    if (prefersReducedMotion) return;
    const qrSteps = document.querySelectorAll('.qr-step');
    const qrStepsEl = document.getElementById('qrSteps');
    if (!qrSteps.length || !qrStepsEl) return;

    const qrObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            qrSteps.forEach((step, i) => {
              setTimeout(() => step.classList.add('visible'), i * 220);
            });
            qrObserver.disconnect();
          }
        });
      },
      { threshold: 0.2 }
    );
    qrObserver.observe(qrStepsEl);
  }

  function easeOutExpo(t) {
    return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
  }

  function animateOdometer(el, target, duration = 1800) {
    const start = performance.now();
    const decimalTarget = el.dataset.decimalTarget;

    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = easeOutExpo(progress);

      if (decimalTarget) {
        const from = parseFloat(decimalTarget) - 0.4;
        const val = (from + (parseFloat(decimalTarget) - from) * eased).toFixed(1);
        el.textContent = val;
      } else {
        el.textContent = Math.round(target * eased);
      }

      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = decimalTarget || String(target);
    }
    requestAnimationFrame(step);
  }

  function initOdometers() {
    if (prefersReducedMotion) return;

    const odometerObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseInt(el.dataset.target, 10);
            if (el.dataset.decimalTarget) {
              el.textContent = (parseFloat(el.dataset.decimalTarget) - 0.4).toFixed(1);
            } else {
              el.textContent = '0';
            }
            animateOdometer(el, target, 1800);
            odometerObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.5 }
    );

    document.querySelectorAll('.odometer').forEach((el) => odometerObserver.observe(el));
  }

  function initSpotlightCards() {
    if (prefersReducedMotion) return;

    document.querySelectorAll('.spotlight-card').forEach((card) => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        card.style.setProperty('--mouse-x', `${x}%`);
        card.style.setProperty('--mouse-y', `${y}%`);
      });
    });
  }

  function initFaq() {
    function toggleFaq(button) {
      const item = button.closest('.faq-item');
      if (!item) return;
      const panel = item.querySelector('.faq-a');
      const isOpen = button.getAttribute('aria-expanded') === 'true';

      document.querySelectorAll('.faq-item').forEach((i) => {
        const q = i.querySelector('.faq-q');
        const a = i.querySelector('.faq-a');
        if (q) q.setAttribute('aria-expanded', 'false');
        if (a) a.hidden = true;
      });

      if (!isOpen && panel) {
        button.setAttribute('aria-expanded', 'true');
        panel.hidden = false;
      }
    }

    document.querySelectorAll('.faq-q').forEach((button) => {
      button.addEventListener('click', () => toggleFaq(button));
    });

    window.toggleFaq = toggleFaq;
  }

  function init() {
    initLenis();
    initNavScroll();
    initDeviceTilt();
    initScrollReveal();
    initQrStagger();
    initOdometers();
    initSpotlightCards();
    initFaq();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
