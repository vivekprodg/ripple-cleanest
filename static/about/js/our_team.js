/* =========================================================
   OUR TEAM - INTERACTION SCRIPT (Django CMS SAFE VERSION)
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // ELEMENT REFERENCES
    // =========================
    const cards = document.querySelectorAll(".member-card");

    const popup = document.getElementById("teamPopup");

    const popupImg = document.getElementById("popupImg");
    const popupName = document.getElementById("popupName");
    const popupRole = document.getElementById("popupRole");
    const popupDesc = document.getElementById("popupDesc");

    const closeBtn = document.getElementById("popupClose");


    // =========================
    // OPEN POPUP ON CARD CLICK
    // =========================
    cards.forEach((card) => {

        card.addEventListener("click", () => {

            const name = card.getAttribute("data-name");
            const role = card.getAttribute("data-role");
            const desc = card.getAttribute("data-desc");
            const img = card.getAttribute("data-img");

            // Fill popup content
            popupName.textContent = name || "";
            popupRole.textContent = role || "";
            popupDesc.textContent = desc || "";
            popupImg.src = img || "";

            // Show popup
            popup.classList.add("active");

            // Prevent background scroll
            document.body.style.overflow = "hidden";
        });

    });


    // =========================
    // CLOSE POPUP FUNCTION
    // =========================
    const closePopup = () => {
        popup.classList.remove("active");

        // Restore scroll
        document.body.style.overflow = "";
    };


    // Close button click
    closeBtn.addEventListener("click", closePopup);


    // Click outside popup box closes it
    popup.addEventListener("click", (e) => {
        if (e.target === popup) {
            closePopup();
        }
    });


    // ESC key closes popup
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && popup.classList.contains("active")) {
            closePopup();
        }
    });

});