document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('image-upload-form');
    const hidden = document.getElementById('pixel-size-hidden');
    // adjust this selector if your slider has a different id
    const slider = document.querySelector('#pixel-size');

    if (slider && hidden) {
      // keep hidden input in sync while user moves the slider
      hidden.value = slider.value;
      slider.addEventListener('input', function (e) {
        hidden.value = e.target.value;
      });
      // also update on change to be safe
      slider.addEventListener('change', function (e) {
        hidden.value = e.target.value;
      });
    }

    // ensure hidden value is present at submit time (works even if slider was removed)
    form.addEventListener('submit', function () {
      if (!hidden.value && slider) hidden.value = slider.value || '';
    });
  });