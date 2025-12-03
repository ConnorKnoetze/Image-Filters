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