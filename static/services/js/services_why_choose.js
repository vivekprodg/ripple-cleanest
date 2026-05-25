/* =========================================================
   WHY CHOOSE US - SERVICES PAGE
   services_why_choose.js
========================================================= */

(function () {

    "use strict";

    const revealElements = document.querySelectorAll(
        '.why-choose-section .reveal'
    );

    if (!revealElements.length) return;

    const revealOnScroll = new IntersectionObserver(
        (entries, observer) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add('active');

                    // Stop observing once animated (performance optimization)
                    observer.unobserve(entry.target);
                }

            });

        },
        {
            threshold: 0.12
        }
    );

    revealElements.forEach(el => {
        revealOnScroll.observe(el);
    });

})();