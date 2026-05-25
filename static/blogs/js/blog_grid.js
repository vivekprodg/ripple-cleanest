/* =========================================
   BLOG GRID SECTION JS
   (layout-level interactions only)
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    const grid = document.querySelector(".blog-grid");

    if (!grid) return;

    const cards = grid.querySelectorAll(".blog-card");

    // OPTIONAL: simple entrance animation hook
    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {
                entry.target.classList.add("in-view");
            }

        });

    }, {
        threshold: 0.15
    });

    cards.forEach(card => {
        observer.observe(card);
    });

});