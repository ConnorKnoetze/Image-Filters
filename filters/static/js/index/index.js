document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector(".carousel-track");
  const slides = document.querySelectorAll(".carousel img");
  if (!track || slides.length === 0) return;

  let index = 0;

  const getSlideWidth = () => {
    const first = slides[0];
    return first.getBoundingClientRect().width || 300;
  };

  const update = () => {
    const width = getSlideWidth();
    track.style.transition = "transform 2s ease";
    track.style.transform = `translateX(-${index * width}px)`;
  };

  const tick = () => {
    index = (index + 1) % slides.length;
    update();
  };

  update();
  window.addEventListener("resize", update);
  setInterval(tick, 3000);
});