(function () {

    // =====================================================
    // SELECT REVEAL ELEMENTS
    // =====================================================
    const revealElements = document.querySelectorAll(
        '.services-hero .reveal'
    );

    // =====================================================
    // EXIT IF NO ELEMENTS FOUND
    // =====================================================
    if (!revealElements.length) {
        return;
    }

    // =====================================================
    // INTERSECTION OBSERVER
    // =====================================================
    const revealOnScroll = new IntersectionObserver(

        (entries, observer) => {

            entries.forEach((entry) => {

                // =============================================
                // ELEMENT ENTERS VIEWPORT
                // =============================================
                if (entry.isIntersecting) {

                    entry.target.classList.add('active');

                    // =========================================
                    // STOP OBSERVING AFTER REVEAL
                    // =========================================
                    observer.unobserve(entry.target);

                }

            });

        },

        {
            threshold: 0.12
        }

    );

    // =====================================================
    // OBSERVE ALL REVEAL ELEMENTS
    // =====================================================
    revealElements.forEach((element) => {

        revealOnScroll.observe(element);

    });

})();