/* =========================================================
   ASSOCIATED WITH — MARQUEE INTERACTION SCRIPT
   Ripple-style hover pause + safety scoped initialization
   ========================================================= */

(function () {
  "use strict";

  /**
   * Wait for DOM safely (prevents null errors in Django includes)
   */
  function initAssociatedWithMarquee() {
    const track = document.querySelector(".assoc-marquee-section .marquee-track");

    if (!track) return; // safely exit if section not loaded

    const marqueeSection = document.querySelector(".assoc-marquee-section");

    if (!marqueeSection) return;

    // ===================== PAUSE ON HOVER =====================
    marqueeSection.addEventListener("mouseenter", function () {
      track.style.animationPlayState = "paused";
    });

    marqueeSection.addEventListener("mouseleave", function () {
      track.style.animationPlayState = "running";
    });

    // ===================== TOUCH SUPPORT (MOBILE UX) =====================
    let isTouched = false;

    marqueeSection.addEventListener("touchstart", function () {
      if (!isTouched) {
        track.style.animationPlayState = "paused";
        isTouched = true;
      }
    });

    marqueeSection.addEventListener("touchend", function () {
      setTimeout(() => {
        track.style.animationPlayState = "running";
        isTouched = false;
      }, 400);
    });

    // ===================== PERFORMANCE OPTIMIZATION =====================
    // Ensure smooth animation restart when tab becomes active again
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) {
        track.style.animationPlayState = "paused";
      } else {
        track.style.animationPlayState = "running";
      }
    });
  }

  // ===================== INIT SAFE =====================
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAssociatedWithMarquee);
  } else {
    initAssociatedWithMarquee();
  }
})();