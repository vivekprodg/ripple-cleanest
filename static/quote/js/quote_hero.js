/* =========================================================
   RFQ HERO SECTION
   Ripple Architecture
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    const hero = document.querySelector(".rfq-hero");

    if (!hero) return;

    const buttons = hero.querySelectorAll(".rfq-hero__button");

    buttons.forEach((button) => {

        button.addEventListener("mouseenter", () => {

            button.style.transform = "translateY(-1px)";

        });

        button.addEventListener("mouseleave", () => {

            button.style.transform = "translateY(0)";

        });

    });

});