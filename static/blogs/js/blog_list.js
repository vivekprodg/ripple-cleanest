document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".blog-card");

    /* stagger reveal on load */
    cards.forEach((card, i) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";

        setTimeout(() => {
            card.style.transition = "all 0.8s cubic-bezier(.19,1,.22,1)";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, i * 120);
    });

    /* optional: subtle parallax hover effect */
    cards.forEach((card) => {
        card.addEventListener("mousemove", (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 25;
            const rotateY = (x - centerX) / 25;

            card.style.transform = `translateY(-12px) rotateX(${ -rotateX }deg) rotateY(${ rotateY }deg)`;
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "";
        });
    });
});