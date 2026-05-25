document.addEventListener("DOMContentLoaded", function () {

    const navbar = document.querySelector(".navbar");
    const navLinks = document.querySelector(".nav-links");
    const menuToggle = document.querySelector(".menu-toggle");

    if (!navbar) return;

    let ticking = false;

    function setTransparent() {
        navbar.classList.add("navbar--transparent");
        navbar.classList.remove("navbar--scrolled");
    }

    function setSticky() {
        navbar.classList.remove("navbar--transparent");
        navbar.classList.add("navbar--scrolled");
    }

    function getHero() {
        return document.querySelector("[data-navbar-hero]");
    }

    function isHeroActive(hero) {
        if (!hero) return false;

        const rect = hero.getBoundingClientRect();

        // STRICT RULE:
        // Navbar stays transparent ONLY while hero top is still below navbar height
        return rect.top < 80 && rect.bottom > 80;
    }

    function updateNavbar() {

        const hero = getHero();

        // If hero exists → hero controls navbar state
        if (hero) {

            if (isHeroActive(hero)) {
                setTransparent();
            } else {
                setSticky();
            }

            return;
        }

        // fallback (no hero pages)
        if (window.scrollY > 10) {
            setSticky();
        } else {
            setTransparent();
        }
    }

    function onScroll() {
        if (ticking) return;

        window.requestAnimationFrame(() => {
            updateNavbar();
            ticking = false;
        });

        ticking = true;
    }

    // IMPORTANT: force correct state AFTER layout stabilizes
    function init() {
        setTimeout(updateNavbar, 0);
        setTimeout(updateNavbar, 100);
    }

    init();

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", updateNavbar);

    if (navLinks) {
        navLinks.addEventListener("click", function (e) {
            if (e.target.closest("a")) {
                navLinks.classList.remove("active");
            }
        });
    }

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });
    }
});