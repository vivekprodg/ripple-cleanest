/* =========================
   BLOG HERO PARALLAX
   SAFE + PERFORMANCE OPTIMIZED
========================= */

document.addEventListener("DOMContentLoaded", () => {

  const img = document.querySelector(".blog-hero__media img");

  if (!img) return;

  const speed = 0.05;
  const baseScale = 1.05;

  let ticking = false;

  function updateParallax() {
    const offset = window.scrollY * speed;

    img.style.transform =
      `translateY(${offset}px) scale(${baseScale})`;

    ticking = false;
  }

  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(updateParallax);
      ticking = true;
    }
  });

});