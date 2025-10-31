document.addEventListener('DOMContentLoaded', () => {
  // copy buttons in dashboard
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.getAttribute('data-clip');
      navigator.clipboard.writeText(text).then(() => {
        const orig = btn.innerText;
        btn.innerText = 'Copied';
        setTimeout(() => btn.innerText = orig, 1200);
      });
    });
  });

  // auto-detect flash links for index page and show copy area (if present)
  // handled server-side via flashed messages; no extra work here
});

