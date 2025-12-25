document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector(".carousel-track");
  const slidesInit = track ? track.querySelectorAll(".slide") : [];
  if (!track || slidesInit.length === 0) return;

  const firstClone = slidesInit[0].cloneNode(true);
  track.appendChild(firstClone);

  let index = 0;

  const getSlideWidth = () => {
    const first = track.querySelector(".slide");
    return (first && first.getBoundingClientRect().width) || 300;
  };

  const update = (withTransition = true) => {
    const width = getSlideWidth();
    track.style.transition = withTransition ? "transform 5s ease" : "none";
    track.style.transform = `translateX(-${index * width}px)`;
  };

  const tick = () => {
    index += 1;
    update(true);

    const total = track.querySelectorAll(".slide").length;
    if (index === total - 1) {
      track.addEventListener(
        "transitionend",
        function handler() {
          track.style.transition = "none";
          index = 0;
          track.style.transform = `translateX(0px)`;
          void track.offsetWidth;
          track.removeEventListener("transitionend", handler);
        },
        { once: true }
      );
    }
  };

  update(false);
  window.addEventListener("resize", () => update(false));
  setInterval(tick, 7000);
});