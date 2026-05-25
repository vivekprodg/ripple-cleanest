// Progress Bar Logic
window.addEventListener('scroll', () => {
    const winScroll =
        document.body.scrollTop ||
        document.documentElement.scrollTop;

    const height =
        document.documentElement.scrollHeight -
        document.documentElement.clientHeight;

    const scrolled = (winScroll / height) * 100;

    document.getElementById("scroll-progress").style.width =
        scrolled + "%";

    // Trigger Reveal Animation
    revealOnScroll();
});

// Simple Intersection Observer-like reveal
function revealOnScroll() {
    const reveals = document.querySelectorAll(".reveal");

    for (let i = 0; i < reveals.length; i++) {
        const windowHeight = window.innerHeight;

        const elementTop =
            reveals[i].getBoundingClientRect().top;

        const elementVisible = 100;

        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add("active");
        }
    }
}

// Run once on load
window.onload = revealOnScroll;