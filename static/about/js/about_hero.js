/* =========================================
   ABOUT HERO SECTION
   FILE: about_hero.js
========================================= */

document.addEventListener('DOMContentLoaded', () => {

    /* =========================
       HERO LOAD ANIMATION
    ========================= */

    const heroContent = document.querySelector('.about-hero-content');

    if (heroContent) {

        setTimeout(() => {
            heroContent.classList.add('active');
        }, 300);

    }

});