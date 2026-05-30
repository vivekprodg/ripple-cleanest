/* =========================================================
   OUR TEAM - INTERACTION SCRIPT
   About page only, scoped, defensive, popup-safe
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    const teamSection = document.querySelector(".about-team-section");
    if (!teamSection) return;

    const cards = teamSection.querySelectorAll(".member-card");
    const popup = teamSection.querySelector("#teamPopup");

    if (!popup) return;

    const popupImg = popup.querySelector("#popupImg");
    const popupName = popup.querySelector("#popupName");
    const popupRole = popup.querySelector("#popupRole");
    const popupDesc = popup.querySelector("#popupDesc");
    const closeBtn = popup.querySelector("#popupClose");

    const socialBlock = popup.querySelector(".social");

    // Force popup hidden on load, even if cache or CSS is inconsistent
    popup.classList.remove("active");
    popup.style.display = "none";
    popup.setAttribute("aria-hidden", "true");

    // Keep popup social icons inside popup only
    if (socialBlock) {
        socialBlock.style.display = "flex";
    }

    const openPopup = (card) => {
        const name = card.getAttribute("data-name") || "";
        const role = card.getAttribute("data-role") || "";
        const desc = card.getAttribute("data-desc") || "";
        const img = card.getAttribute("data-img") || "";

        if (popupName) popupName.textContent = name;
        if (popupRole) popupRole.textContent = role;
        if (popupDesc) popupDesc.textContent = desc;
        if (popupImg) popupImg.src = img;

        popup.style.display = "flex";
        popup.classList.add("active");
        popup.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";
    };

    const closePopup = () => {
        popup.classList.remove("active");
        popup.style.display = "none";
        popup.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";

        if (popupImg) popupImg.src = "";
        if (popupName) popupName.textContent = "";
        if (popupRole) popupRole.textContent = "";
        if (popupDesc) popupDesc.textContent = "";
    };

    cards.forEach((card) => {
        card.setAttribute("role", "button");
        card.setAttribute("tabindex", "0");

        card.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            openPopup(card);
        });

        card.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                openPopup(card);
            }
        });

        const img = card.querySelector("img");
        if (img) {
            img.setAttribute("draggable", "false");
            img.addEventListener("click", (e) => {
                e.preventDefault();
                e.stopPropagation();
                openPopup(card);
            });
        }
    });

    if (closeBtn) {
        closeBtn.addEventListener("click", closePopup);
    }

    popup.addEventListener("click", (e) => {
        if (e.target === popup) {
            closePopup();
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && popup.classList.contains("active")) {
            closePopup();
        }
    });
});