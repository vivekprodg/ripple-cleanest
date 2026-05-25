/* =========================================================
   INTERIOR GALLERY - FILTER + MODAL SYSTEM
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* ================= FILTER SYSTEM ================= */

    const filterButtons = document.querySelectorAll(
        ".interior-gallery-section .filter-btn"
    );

    const galleryItems = document.querySelectorAll(
        ".interior-gallery-section .gallery-item"
    );

    if (filterButtons.length && galleryItems.length) {

        filterButtons.forEach(button => {

            button.addEventListener("click", () => {

                filterButtons.forEach(btn => {
                    btn.classList.remove("active");
                });

                button.classList.add("active");

                const filterValue = button.getAttribute("data-filter");

                galleryItems.forEach(item => {

                    const category = item.getAttribute("data-category");

                    if (filterValue === "all" || category === filterValue) {
                        item.classList.remove("hide");
                    } else {
                        item.classList.add("hide");
                    }

                });

            });

        });

    }

    /* ================= CARD CLICK HANDLER ================= */

    document.querySelectorAll(".gallery-item").forEach(item => {

        item.addEventListener("click", function () {

            openModal(
                this.dataset.img || "",
                this.dataset.title || "",
                this.dataset.desc || "",
                this.dataset.categoryLabel || "",
                this.dataset.location || "",
                this.dataset.year || "",
                this.dataset.client || ""
            );

        });

    });

});


/* =========================================================
   MODAL SYSTEM (GLOBAL FUNCTIONS)
========================================================= */

/**
 * Open gallery modal with project data
 */
function openModal(img, title, desc, category, location, year, client) {

    const modal = document.getElementById("galleryModal");

    if (!modal) return;

    modal.classList.add("active");

    document.getElementById("modalImg").src = img || "";
    document.getElementById("modalTitle").innerText = title || "";
    document.getElementById("modalDesc").innerText = desc || "";

    document.getElementById("modalCategory").innerText = category || "";

    document.getElementById("detailCategory").innerText = category || "";
    document.getElementById("detailLocation").innerText = location || "";
    document.getElementById("detailYear").innerText = year || "";
    document.getElementById("detailClient").innerText = client || "";

    document.body.style.overflow = "hidden";
}


/**
 * Close gallery modal
 */
function closeModal() {

    const modal = document.getElementById("galleryModal");

    if (!modal) return;

    modal.classList.remove("active");

    document.body.style.overflow = "auto";
}


/* =========================================================
   ESC KEY CLOSE SUPPORT
========================================================= */
document.addEventListener("keydown", function (e) {

    if (e.key === "Escape") {
        closeModal();
    }

});