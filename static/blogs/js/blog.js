// =============================
// BLOG PAGE CONTROLLER ONLY
// Progress bar only
// =============================

(function () {
    "use strict";

    function updateProgressBar() {
        const progressBar = document.getElementById("progress-bar");
        if (!progressBar) return;

        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const docHeight =
            document.documentElement.scrollHeight -
            document.documentElement.clientHeight;

        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progressBar.style.width = progress + "%";
    }

    document.addEventListener("DOMContentLoaded", function () {
        updateProgressBar();
    });

    window.addEventListener("scroll", updateProgressBar, { passive: true });
    window.addEventListener("resize", updateProgressBar);
})();