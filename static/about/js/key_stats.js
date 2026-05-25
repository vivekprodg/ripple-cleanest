/* =========================
   KEY STATS COUNTER ANIMATION
========================= */

document.addEventListener('DOMContentLoaded', () => {

    const statsWrapper = document.getElementById('stats-counter-wrapper');
    const counters = document.querySelectorAll('.count-up');

    const duration = 2200;

    /* =========================
       EASING FUNCTION
    ========================= */
    const easeOutExpo = (t) => {
        return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
    };

    /* =========================
       ANIMATE SINGLE COUNTER
    ========================= */
    const animateValue = (el) => {

        const target = parseInt(el.dataset.target, 10);

        if (isNaN(target)) return;

        let startTime = null;

        const updateCounter = (currentTime) => {

            if (!startTime) startTime = currentTime;

            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const eased = easeOutExpo(progress);

            const value = Math.floor(eased * target);

            el.textContent = value;

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                el.textContent = target;
            }
        };

        requestAnimationFrame(updateCounter);
    };

    /* =========================
       OBSERVER (TRIGGER ON VIEW)
    ========================= */
    const observer = new IntersectionObserver((entries, observer) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                counters.forEach(counter => {
                    animateValue(counter);
                });

                observer.unobserve(entry.target);
            }
        });

    }, {
        threshold: 0.25
    });

    /* =========================
       INIT OBSERVER
    ========================= */
    if (statsWrapper) {
        observer.observe(statsWrapper);
    }

});