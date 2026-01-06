function bindSlider(sliderEl, displayEl, options = {}) {
  const format = options.format || (v => v);
  const onChange = typeof options.onChange === 'function' ? options.onChange : null;

  function update(value, emit = true) {
    const formatted = format(value);
    if (displayEl) displayEl.textContent = formatted;
    sliderEl.setAttribute('aria-valuenow', value);
    sliderEl.dataset.value = value;
    if (emit) {
      sliderEl.dispatchEvent(new CustomEvent('slider:change', {
        detail: { value: Number(value), formatted },
        bubbles: true
      }));
      if (onChange) onChange(Number(value));
    }
  }

  // initialize
  update(sliderEl.value, false);

  // live update while dragging
  sliderEl.addEventListener('input', (e) => update(e.target.value, true));
  // final change (optional)
  sliderEl.addEventListener('change', (e) => update(e.target.value, true));

  return {
    update: (v) => update(v, true)
  };
}

function initSliders(root = document) {
  const sliders = Array.from(root.querySelectorAll('input[type="range"]'));
  const instances = [];
  sliders.forEach(slider => {
    // target selector in data-slider-target or look for sibling .slider-value
    const targetSel = slider.dataset.sliderTarget;
    let display = null;
    if (targetSel) display = root.querySelector(targetSel);
    if (!display) {
      // try sibling or next element with class 'slider-value'
      display = slider.parentElement?.querySelector('.slider-value') ||
                slider.nextElementSibling?.matches?.('.slider-value') ? slider.nextElementSibling : null;
      if (display && !display.matches('.slider-value')) display = null;
    }
    const formatterName = slider.dataset.format; // e.g. "percent"
    const format = (val => {
      if (formatterName === 'percent') return `${val}%`;
      if (formatterName === 'float') return parseFloat(val).toFixed(2);
      return val;
    });
    const inst = bindSlider(slider, display, { format });
    instances.push({ slider, display, instance: inst });
  });
  return instances;
}

// expose for other pages
window.FilterSlider = { bindSlider, initSliders };