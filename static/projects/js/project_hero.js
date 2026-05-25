 /* =========================================================
   PROJECT HERO JS
   Ripple CMS - Projects Module
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    const heroContent = document.querySelector(".project-hero__content");

    if (!heroContent) return; // safety guard (CMS-safe)

    /* ================= HERO ENTRANCE ANIMATION ================= */

    heroContent.animate(
        [
            {
                opacity: 0,
                transform: "translateY(40px)"
            },
            {
                opacity: 1,
                transform: "translateY(0)"
            }
        ],
        {
            duration: 1000,
            easing: "ease-out",
            fill: "forwards"
        }
    );

});