/* =========================================
   INTERIOR PHILOSOPHY SECTION
========================================= */

document.addEventListener('DOMContentLoaded', () => {

    const philosophyImages = document.querySelectorAll(
        '.philosophy-media img'
    );

    philosophyImages.forEach((img) => {

        img.addEventListener('mouseenter', () => {

            img.style.filter = 'brightness(1.05)';

        });

        img.addEventListener('mouseleave', () => {

            img.style.filter = 'brightness(1)';

        });

    });

});