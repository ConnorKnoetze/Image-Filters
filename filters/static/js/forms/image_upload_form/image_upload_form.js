document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('image-upload-form');
  if (!form) return;

  // Keep existing explicit hidden pixel_size if present
  const existingHidden = document.getElementById('pixel-size-hidden');

  // Find all sliders on the page
  const sliders = Array.from(document.querySelectorAll('input[type="range"]'));

  sliders.forEach(slider => {
    // skip if slider is already inside the form (will submit naturally)
    if (slider.closest('form') === form) return;

    const sliderName = slider.name;
    if (!sliderName) return;

    // ensure a hidden input with the same name exists in the form
    let hidden = form.querySelector(`input[type="hidden"][name="${sliderName}"]`);
    if (!hidden) {
      hidden = document.createElement('input');
      hidden.type = 'hidden';
      hidden.name = sliderName;
      form.appendChild(hidden);
    }

    // also create underscore-normalized hidden input (for central handlers expecting pixel_size)
    const normalized = sliderName.replace(/-/g, '_');
    let normHidden = null;
    if (normalized !== sliderName) {
      normHidden = form.querySelector(`input[type="hidden"][name="${normalized}"]`);
      if (!normHidden) {
        normHidden = document.createElement('input');
        normHidden.type = 'hidden';
        normHidden.name = normalized;
        // keep id for compatibility if there is an existing pixel-size-hidden
        if (normalized === 'pixel_size' && existingHidden) {
          // reuse existing hidden input element
          normHidden = existingHidden;
        } else {
          form.appendChild(normHidden);
        }
      }
    }

    // initialize
    hidden.value = slider.value;
    if (normHidden) normHidden.value = slider.value;

    // sync on input/change
    slider.addEventListener('input', (e) => {
      hidden.value = e.target.value;
      if (normHidden) normHidden.value = e.target.value;
    });
    slider.addEventListener('change', (e) => {
      hidden.value = e.target.value;
      if (normHidden) normHidden.value = e.target.value;
    });
  });

  // ensure hidden values are present at submit time
  form.addEventListener('submit', function () {
    // for sliders inside form, nothing to do
    // for outside sliders we've already set hidden inputs; ensure any existing hidden sync (defensive)
    const inputs = Array.from(document.querySelectorAll('input[type="range"]'));
    inputs.forEach(slider => {
      const name = slider.name;
      if (!name) return;
      const h = form.querySelector(`input[type="hidden"][name="${name}"]`);
      if (h) h.value = slider.value;
      const normalized = name.replace(/-/g, '_');
      const hn = form.querySelector(`input[type="hidden"][name="${normalized}"]`);
      if (hn) hn.value = slider.value;
    });
  });
});

(function () {
  function findForms() {
    const byClass = Array.from(document.querySelectorAll('form.image-upload-form'));
    const byId = document.getElementById('image-upload-form');
    if (byId && !byClass.includes(byId)) byClass.push(byId);
    return byClass;
  }

  function ensureOverlay(form) {
    let overlay = form.querySelector('.upload-loading-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'upload-loading-overlay';
      overlay.setAttribute('aria-hidden', 'true');
      overlay.hidden = true;
      overlay.innerHTML = '<div class="upload-loading-box" role="status" aria-live="polite"><div class="upload-spinner" aria-hidden="true"></div><div class="upload-loading-text">Uploading\u2026</div></div>';
      form.style.position = form.style.position || 'relative';
      form.appendChild(overlay);
    }
    return overlay;
  }

  function toggleElements(form, disabled) {
    Array.from(form.querySelectorAll('input, button, select, textarea')).forEach(el => {
      // keep file input enabled (optional) but disable to prevent double submits
      if (el.type === 'file') el.disabled = disabled;
      else el.disabled = disabled;
    });
  }

  function showLoading(form, message) {
    const overlay = ensureOverlay(form);
    const text = overlay.querySelector('.upload-loading-text');
    if (message) text.textContent = message;
    overlay.hidden = false;
    overlay.setAttribute('aria-hidden', 'false');
    toggleElements(form, true);
    // accessibility
    form.setAttribute('aria-busy', 'true');
    // fallback: re-enable after 30s if nothing happens (prevents permanent lock)
    form.__uploadTimeout = setTimeout(() => hideLoading(form), 30000);
  }

  function hideLoading(form) {
    const overlay = form.querySelector('.upload-loading-overlay');
    if (!overlay) return;
    overlay.hidden = true;
    overlay.setAttribute('aria-hidden', 'true');
    toggleElements(form, false);
    form.removeAttribute('aria-busy');
    if (form.__uploadTimeout) {
      clearTimeout(form.__uploadTimeout);
      form.__uploadTimeout = null;
    }
  }

  // auto-bind
  document.addEventListener('DOMContentLoaded', function () {
    const forms = findForms();
    forms.forEach(form => {
      ensureOverlay(form);
      form.addEventListener('submit', function (e) {
        // If the submit was prevented by client code, do not show the overlay
        // Delay slightly to allow synchronous validation code to run
        setTimeout(() => {
          if (!e.defaultPrevented) showLoading(form);
        }, 10);
      }, { passive: true });
    });
  });

  // expose globally for manual control (e.g. when using fetch/XHR)
  window.ImageUpload = {
    showLoading: function (formOrSelector, message) {
      const form = typeof formOrSelector === 'string' ? document.querySelector(formOrSelector) : formOrSelector;
      if (!form) return;
      showLoading(form, message);
    },
    hideLoading: function (formOrSelector) {
      const form = typeof formOrSelector === 'string' ? document.querySelector(formOrSelector) : formOrSelector;
      if (!form) return;
      hideLoading(form);
    }
  };

  // Hide overlay on navigation/back/forward to keep UI consistent
  window.addEventListener('pageshow', () => {
    findForms().forEach(f => hideLoading(f));
  });
})();