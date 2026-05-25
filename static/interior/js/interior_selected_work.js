// ================= SELECTED WORK CMS MODAL =================

document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".js-work-card");

    cards.forEach((card) => {
        card.addEventListener("click", () => {
            openModal(
                card.dataset.img || "",
                card.dataset.title || "",
                card.dataset.desc || ""
            );
        });
    });
});

function openModal(img, title, desc) {
    const modal = document.getElementById("modal");
    const mimg = document.getElementById("mimg");
    const mtitle = document.getElementById("mtitle");
    const mdesc = document.getElementById("mdesc");

    if (!modal || !mimg || !mtitle || !mdesc) {
        return;
    }

    modal.style.display = "flex";
    mimg.src = img || "";
    mtitle.innerText = title || "";
    mdesc.innerText = desc || "";
}