/* =========================================================
   HOME JOURNAL SECTION
   FILE: static/home/js/journal.js
========================================================= */

document.addEventListener('DOMContentLoaded', () => {

    const revealElements = document.querySelectorAll('.hp-reveal');

    if (!revealElements.length) return;

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries, obs) => {

        entries.forEach((entry) => {

            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                obs.unobserve(entry.target); // run once for performance
            }

        });

    }, observerOptions);

    revealElements.forEach((el, index) => {

        // Stagger animation like your original design
        el.style.transitionDelay = `${index * 0.15}s`;

        observer.observe(el);

    });

});