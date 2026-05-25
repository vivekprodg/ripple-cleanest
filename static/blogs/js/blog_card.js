/* =========================================
   BLOG CARD INTERACTIONS
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(".blog-card");

    if (!cards.length) return;

    cards.forEach(card => {

        /* =========================================
           MOUSEMOVE LIGHT EFFECT
        ========================================= */

        card.addEventListener("mousemove", (e) => {

            const rect = card.getBoundingClientRect();

            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.background = `
                radial-gradient(
                    circle at ${x}px ${y}px,
                    rgba(0,0,0,0.03),
                    #ffffff 55%
                )
            `;

        });

        /* =========================================
           RESET BACKGROUND
        ========================================= */

        card.addEventListener("mouseleave", () => {

            card.style.background = `
                linear-gradient(
                    180deg,
                    #ffffff,
                    #faf8f3
                )
            `;

        });

    });

});