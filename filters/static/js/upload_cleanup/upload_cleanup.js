(function () {
  'use strict';

  const el = document.getElementById('upload-cleanup');
  if (!el) return;

  let filenames = [];
  try {
    const raw = el.getAttribute('data-uploaded-filenames') || '[]';
    filenames = JSON.parse(raw).filter(Boolean);
  } catch (err) {
    filenames = [];
  }
  if (!filenames.length) return;

  const deleteUrl = el.getAttribute('data-delete-url');
  if (!deleteUrl) return;

  let sent = false;
  function sendDelete() {
    if (sent) return;
    sent = true;
    const payload = JSON.stringify({ filenames });

    try {
      if (navigator.sendBeacon) {
        const blob = new Blob([payload], { type: 'application/json' });
        navigator.sendBeacon(deleteUrl, blob);
        return;
      }
    } catch (e) {
      // fallthrough to fetch
    }

    // fallback: keepalive helps during unload
    fetch(deleteUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: payload,
      keepalive: true
    }).catch(() => { /* best-effort */ });
  }

  window.addEventListener('pagehide', sendDelete, { capture: true, passive: true });
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') sendDelete();
  });
  window.addEventListener('beforeunload', sendDelete);
})();