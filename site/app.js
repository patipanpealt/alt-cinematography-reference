/* A Cinematography Reference — interactions */
(function () {
  'use strict';

  /* ---------- Lightbox ---------- */
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lightbox-img');
  var lbClose = lb.querySelector('.lightbox-close');
  var lastFocused = null;

  function openLightbox(src, alt) {
    lastFocused = document.activeElement;
    lbImg.src = src;
    lbImg.alt = alt || '';
    lb.classList.add('open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.classList.add('lb-open');
    lbClose.focus();
  }

  function closeLightbox() {
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('lb-open');
    lbImg.removeAttribute('src');
    if (lastFocused) lastFocused.focus();
  }

  document.querySelectorAll('[data-zoom]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var img = btn.querySelector('img');
      openLightbox(img.getAttribute('src'), img.getAttribute('alt'));
    });
  });

  lbClose.addEventListener('click', closeLightbox);
  lb.addEventListener('click', function (e) {
    if (e.target === lb || e.target.classList.contains('lightbox-inner')) closeLightbox();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lb.classList.contains('open')) closeLightbox();
  });

  /* ---------- Scroll-driven chrome ----------
     Two earlier attempts here were both timing-fragile: a requestAnimationFrame guard
     that stuck permanently when a frame was dropped, and a cached hero height measured
     before the webfonts landed, which left the threshold far too high. So the button now
     keys off an IntersectionObserver on the hero (no measurement at all), and the nav's
     cached offsets are refreshed by a ResizeObserver whenever the document reflows. */
  var toTop = document.getElementById('to-top');
  var hero = document.getElementById('hero');
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-links a'));
  var sections = navLinks
    .map(function (a) {
      var el = document.querySelector(a.getAttribute('href'));
      return el ? { link: a, el: el, top: 0 } : null;
    })
    .filter(Boolean);

  /* show the button once the hero has scrolled out of view */
  if ('IntersectionObserver' in window && hero) {
    new IntersectionObserver(function (entries) {
      toTop.classList.toggle('show', !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(hero);
  } else {
    window.addEventListener('scroll', function () {
      toTop.classList.toggle('show', window.scrollY > window.innerHeight * 0.75);
    }, { passive: true });
  }

  toTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* nav active state — a plain scroll handler that reads offsetTop live.
     Caching the offsets went stale before the webfonts landed, and an
     IntersectionObserver band missed sections on fast jumps, so this reads the six
     values each time: they are read-only lookups and never force a reflow. */
  var activeLink = null;

  function setActive(link) {
    if (link === activeLink) return;
    if (activeLink) activeLink.classList.remove('active');
    if (link) link.classList.add('active');
    activeLink = link;
  }

  function syncNav() {
    var probe = window.scrollY + 100;   // just under the floating nav
    var current = null;
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].el.offsetTop <= probe) current = sections[i];
    }
    setActive(current ? current.link : null);
  }

  window.addEventListener('scroll', syncNav, { passive: true });
  window.addEventListener('resize', syncNav);
  window.addEventListener('load', syncNav);
  syncNav();
})();
