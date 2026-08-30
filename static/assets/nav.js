(function () {
  var btn = document.getElementById('nav-toggle');
  if (!btn) return;

  var links = document.getElementById('nav-links');

  function setOpen(open) {
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (document.body.classList) {
      document.body.classList.toggle('nav-open', open);
    }
  }

  btn.addEventListener('click', function () {
    setOpen(btn.getAttribute('aria-expanded') !== 'true');
  });

  // Close the menu after choosing a destination link.
  if (links) {
    links.addEventListener('click', function (e) {
      var target = e.target && e.target.closest ? e.target.closest('a') : null;
      if (target) setOpen(false);
    });
  }

  // Close on Escape and return focus to the toggle.
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      btn.focus();
    }
  });
})();
