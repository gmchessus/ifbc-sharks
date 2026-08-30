(() => {
  const heroImage = document.querySelector('.hero-shot img');
  if (!heroImage || !Array.isArray(window.SHARKS_MEDIA)) return;

  const candidates = window.SHARKS_MEDIA.filter((item) => item.src);
  const image = candidates.find((item) => item.src.includes('/upload/iblock/'));
  if (image) {
    heroImage.src = image.src.replace('../archive/', '/archive/');
    heroImage.alt = image.alt || 'Архивное фото ИФБК «Акулы»';
  }
})();

(() => {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.nav-links');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', () => {
    const open = toggle.classList.toggle('is-open');
    nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      toggle.classList.remove('is-open');
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });
})();
