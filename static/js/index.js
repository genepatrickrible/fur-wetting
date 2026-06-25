// Cite dropdown: toggle on click; close on outside-click or Escape.
// "Copy as text" writes both text/plain and text/html so paste targets that
// respect rich text (Word, Google Docs, Notes, email) get italics on the
// journal name and bold on the volume number; plain-text contexts get the
// unformatted string.

(function () {
  const dropdown = document.querySelector('.cite-dropdown');
  if (!dropdown) return;
  const trigger = dropdown.querySelector('.dropdown-trigger button');
  const copyItem = dropdown.querySelector('[data-cite-text]');
  const copyLabel = copyItem && copyItem.querySelector('.cite-label');

  function open() { dropdown.classList.add('is-active'); }
  function close() { dropdown.classList.remove('is-active'); }
  function toggle() { dropdown.classList.toggle('is-active'); }

  if (trigger) {
    trigger.addEventListener('click', (e) => { e.stopPropagation(); toggle(); });
  }

  document.addEventListener('click', (e) => {
    if (!dropdown.contains(e.target)) close();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });

  async function copyCitation(text, html) {
    try {
      if (navigator.clipboard && typeof window.ClipboardItem !== 'undefined') {
        const item = new ClipboardItem({
          'text/plain': new Blob([text], { type: 'text/plain' }),
          'text/html': new Blob([html], { type: 'text/html' })
        });
        await navigator.clipboard.write([item]);
        return;
      }
      await navigator.clipboard.writeText(text);
      return;
    } catch {
      // Older browsers: hidden textarea + execCommand. Loses formatting.
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
  }

  if (copyItem) {
    copyItem.addEventListener('click', async (e) => {
      e.preventDefault();
      const text = copyItem.dataset.citationText || '';
      const html = copyItem.dataset.citationHtml || text;
      await copyCitation(text, html);
      if (copyLabel) {
        const original = copyLabel.textContent;
        copyLabel.textContent = 'Copied!';
        setTimeout(() => { copyLabel.textContent = original; close(); }, 1200);
      } else {
        close();
      }
    });
  }
})();

// Figure lightbox: click any figure image to enlarge it; click the overlay,
// press Escape, or click the close button to dismiss. Applies to every
// <figure class="image"><img> on the page (result figures, paired panels,
// pre-figure images, the firsts intro image). Images that are wrapped in a
// link (e.g. the hub journal-cover) are left alone so their link still works.
(function () {
  const imgs = Array.prototype.slice
    .call(document.querySelectorAll('figure.image img'))
    .filter((img) => !img.closest('a'));
  if (!imgs.length) return;

  let overlay, overlayImg;

  function buildOverlay() {
    overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.innerHTML =
      '<button class="lightbox-close" aria-label="Close">&times;</button>' +
      '<img class="lightbox-img" alt="">' +
      '<p class="lightbox-caption"></p>';
    overlayImg = overlay.querySelector('.lightbox-img');
    const caption = overlay.querySelector('.lightbox-caption');
    overlay.addEventListener('click', (e) => {
      // close on backdrop or close-button click, but not when clicking the image
      if (e.target !== overlayImg) closeLightbox();
    });
    document.body.appendChild(overlay);
    overlay._caption = caption;
  }

  function openLightbox(src, alt) {
    if (!overlay) buildOverlay();
    overlayImg.src = src;
    overlayImg.alt = alt || '';
    overlay._caption.textContent = alt || '';
    overlay.classList.add('is-active');
    document.body.classList.add('lightbox-open');
  }

  function closeLightbox() {
    if (!overlay) return;
    overlay.classList.remove('is-active');
    document.body.classList.remove('lightbox-open');
  }

  imgs.forEach((img) => {
    img.classList.add('is-zoomable');
    img.addEventListener('click', () => {
      // prefer a high-res source if one is provided, else the displayed src
      openLightbox(img.getAttribute('data-full') || img.currentSrc || img.src, img.alt);
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });
})();
