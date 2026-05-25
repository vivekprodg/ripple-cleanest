(function () {

    "use strict";

    /* =========================================
       REVEAL ANIMATION
    ========================================= */

    const revealElements = document.querySelectorAll('.reveal');

    if (revealElements.length) {

        const revealObserver = new IntersectionObserver((entries, observer) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target);
                }

            });

        }, {
            threshold: 0.12,
            rootMargin: '0px 0px -40px 0px'
        });

        revealElements.forEach((element, index) => {
            element.style.transitionDelay = `${index * 0.05}s`;
            revealObserver.observe(element);
        });

    }

    /* =========================================
       FAQ ACCORDION (ROBUST FIX)
    ========================================= */

    const accordionItems = document.querySelectorAll('.accordion-item');

    const closeItem = (item) => {
        item.classList.remove('active');

        const panel = item.querySelector('.accordion-panel');
        if (panel) {
            panel.style.maxHeight = "0px";
        }
    };

    const openItem = (item) => {
        item.classList.add('active');

        const panel = item.querySelector('.accordion-panel');
        if (!panel) return;

        // force correct recalculation
        panel.style.maxHeight = "none";
        const height = panel.scrollHeight;

        panel.style.maxHeight = "0px";

        requestAnimationFrame(() => {
            panel.style.maxHeight = height + "px";
        });
    };

    if (accordionItems.length) {

        accordionItems.forEach(item => {

            const button = item.querySelector('.accordion-button');
            const panel = item.querySelector('.accordion-panel');

            if (!button || !panel) return;

            panel.style.maxHeight = "0px";

            button.addEventListener('click', () => {

                const isActive = item.classList.contains('active');

                accordionItems.forEach(closeItem);

                if (!isActive) {
                    openItem(item);
                }

            });

        });

        window.addEventListener('load', () => {
            document.querySelectorAll('.accordion-item.active').forEach(openItem);
        });

        window.addEventListener('resize', () => {
            document.querySelectorAll('.accordion-item.active').forEach(openItem);
        });

    }

    /* =========================================
       OPTIONAL PARALLAX EFFECT
    ========================================= */

    const spotlightImage = document.querySelector('.spotlight-card.image');

    if (spotlightImage && window.innerWidth > 991) {

        window.addEventListener('scroll', () => {
            const rect = spotlightImage.getBoundingClientRect();
            const offset = rect.top * -0.04;
            spotlightImage.style.backgroundPosition = `center calc(50% + ${offset}px)`;
        });

    }

})();