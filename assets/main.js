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
