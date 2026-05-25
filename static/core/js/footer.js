/**
 * Ripple Footer JS
 * CMS-safe + Django-safe implementation
 * Handles:
 * - Year update fallback (if not handled in template)
 * - Newsletter form interaction
 * - Graceful DOM checks (important for CMS rendering)
 */

(function () {
    "use strict";

    /* =========================
       AUTO YEAR FALLBACK
       (only runs if span exists)
    ========================= */
    const yearEl = document.getElementById("current-year");
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    /* =========================
       NEWSLETTER FORM HANDLING
       CMS SAFE (no backend dependency)
    ========================= */
    const form = document.querySelector(".newsletter-form");

    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const button = form.querySelector("button");
            const input = form.querySelector("input[type='email']");

            if (!button || !input) return;

            // Preserve original text (CMS-safe restore)
            const originalText = button.textContent;

            // UI feedback (Ripple-style minimal interaction)
            button.textContent = "Sent";
            button.style.opacity = "0.7";
            button.style.color = "#ffffff";

            // Reset input
            input.value = "";

            // Restore after short delay
            setTimeout(() => {
                button.textContent = originalText;
                button.style.opacity = "1";
            }, 2000);
        });
    }

    /* =========================
       SMOOTH SOCIAL LINK FEEL
       (optional enhancement, safe)
    ========================= */
    const socialLinks = document.querySelectorAll(".social-links a");

    if (socialLinks.length > 0) {
        socialLinks.forEach(link => {
            link.addEventListener("mouseenter", () => {
                link.style.transition = "transform 0.3s ease, color 0.3s ease";
            });
        });
    }

    /* =========================
       SAFE LOG (DEV ONLY)
    ========================= */
    if (window.location.hostname === "localhost") {
        console.log("[Ripple Footer] Loaded successfully");
    }

})();