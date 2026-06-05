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
