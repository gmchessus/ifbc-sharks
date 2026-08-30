const media = Array.isArray(window.SHARKS_MEDIA) ? window.SHARKS_MEDIA : [];
const grid = document.querySelector('#archive-grid');
const more = document.querySelector('#archive-more');
const search = document.querySelector('#archive-search');
const count = document.querySelector('#archive-count');
const lightbox = document.querySelector('#archive-lightbox');
const large = document.querySelector('#archive-large');
const source = document.querySelector('#archive-source');
const pageSize = 40;
let visible = pageSize;
let filtered = media;

function createTile(item) {
  const button = document.createElement('button');
  button.className = 'archive-tile';
  button.type = 'button';
  button.setAttribute('aria-label', 'Открыть фото из архива');

  const image = document.createElement('img');
  image.loading = 'lazy';
  image.decoding = 'async';
  image.alt = item.alt || 'Архивное фото ИФБК «Акулы»';
  image.src = item.src.replace('../archive/', '/archive/');
  button.append(image);
  button.addEventListener('click', () => {
    large.src = image.src;
    large.alt = image.alt;
    source.textContent = item.source || '';
    lightbox.hidden = false;
  });
  return button;
}

function render(reset = false) {
  if (reset) visible = pageSize;
  grid.replaceChildren();
  filtered.slice(0, visible).forEach((item) => grid.append(createTile(item)));
  count.textContent = `${filtered.length} фото · показано ${Math.min(visible, filtered.length)}`;
  more.hidden = visible >= filtered.length;
}

function filter() {
  const query = search.value.trim().toLowerCase();
  filtered = media.filter((item) => `${item.src} ${item.source}`.toLowerCase().includes(query));
  render(true);
}

let searchTimer;
search.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(filter, 180);
});
more.addEventListener('click', () => {
  visible += pageSize;
  render();
});
document.querySelector('#archive-close').addEventListener('click', () => {
  lightbox.hidden = true;
});
lightbox.addEventListener('click', (event) => {
  if (event.target === lightbox) lightbox.hidden = true;
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') lightbox.hidden = true;
});
render(true);
