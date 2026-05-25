/* =========================================
   CLIENT TESTIMONIALS SLIDER
========================================= */

document.addEventListener('DOMContentLoaded', () => {

    /* =========================================
       ELEMENT REFERENCES
    ========================================= */

    const viewport = document.getElementById('carousel-viewport');

    const slides = document.querySelectorAll(
        '.premium-patron-card'
    );

    const progressLine = document.getElementById(
        'lux-progress-indicator'
    );

    /* =========================================
       SAFETY CHECK
    ========================================= */

    if (!viewport || !slides.length || !progressLine) {
        return;
    }

    /* =========================================
       SLIDER STATE
    ========================================= */

    let currentSlideIndex = 0;

    const totalSlidesCount = slides.length;

    let autoSliderTimer = null;

    const autoPlayDuration = 5000;

    /* =========================================
       UPDATE ACTIVE SLIDE
    ========================================= */

    const updateSliderState = (index) => {

        /* REMOVE CURRENT ACTIVE */

        slides[currentSlideIndex].classList.remove(
            'active'
        );

        /* UPDATE INDEX */

        currentSlideIndex = index;

        /* UPDATE PROGRESS LINE */

        const percentPosition =
            ((currentSlideIndex + 1) / totalSlidesCount) * 100;

        progressLine.style.width = `${percentPosition}%`;

        /* ACTIVATE TARGET SLIDE */

        slides[currentSlideIndex].classList.add(
            'active'
        );

    };

    /* =========================================
       NEXT SLIDE
    ========================================= */

    const advanceSlideNext = () => {

        let nextIndex = currentSlideIndex + 1;

        if (nextIndex >= totalSlidesCount) {
            nextIndex = 0;
        }

        updateSliderState(nextIndex);

    };

    /* =========================================
       AUTOPLAY START
    ========================================= */

    const initializeAutoPlayCycle = () => {

        if (autoSliderTimer === null) {

            autoSliderTimer = setInterval(
                advanceSlideNext,
                autoPlayDuration
            );

        }

    };

    /* =========================================
       AUTOPLAY STOP
    ========================================= */

    const clearAutoPlayCycle = () => {

        if (autoSliderTimer !== null) {

            clearInterval(autoSliderTimer);

            autoSliderTimer = null;

        }

    };

    /* =========================================
       HOVER INTERACTION
    ========================================= */

    viewport.addEventListener(
        'mouseenter',
        clearAutoPlayCycle
    );

    viewport.addEventListener(
        'mouseleave',
        initializeAutoPlayCycle
    );

    /* =========================================
       INITIALIZE SLIDER
    ========================================= */

    updateSliderState(0);

    initializeAutoPlayCycle();

});