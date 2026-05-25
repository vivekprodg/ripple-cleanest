/* ========================================
   VISION / MISSION / VALUES SECTION
======================================== */

document.addEventListener("DOMContentLoaded", () => {

    const pillarCards = document.querySelectorAll(".pillar-card");

    if (!pillarCards.length) return;

    /* ========================================
       REVEAL ANIMATION
    ======================================== */

    const revealCards = new IntersectionObserver((entries) => {

        entries.forEach((entry, index) => {

            if (entry.isIntersecting) {

                setTimeout(() => {

                    entry.target.classList.add("pillar-visible");

                }, index * 150);

            }

        });

    }, {
        threshold: 0.15
    });

    pillarCards.forEach((card) => {

        card.classList.add("pillar-hidden");

        revealCards.observe(card);

    });

    /* ========================================
       MOUSE MOVE GLOW EFFECT
    ======================================== */

    pillarCards.forEach((card) => {

        card.addEventListener("mousemove", (e) => {

            const rect = card.getBoundingClientRect();

            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.setProperty("--x", `${x}px`);
            card.style.setProperty("--y", `${y}px`);

        });

    });

});