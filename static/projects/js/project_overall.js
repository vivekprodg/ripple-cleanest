let status = "all";
let category = "all";
let currentProjectId = null;

/* ================= UTILITY ================= */
function getCards() {
    return document.querySelectorAll(".card");
}

/* ================= STATUS FILTER ================= */
document.addEventListener("click", function (e) {

    const btn = e.target.closest("[data-status]");
    if (!btn) return;

    document.querySelectorAll("[data-status]").forEach(b => {
        b.classList.remove("active");
    });

    btn.classList.add("active");

    status = btn.dataset.status;
    filter();
});

/* ================= CATEGORY FILTER ================= */
document.addEventListener("click", function (e) {

    const btn = e.target.closest(".cat");
    if (!btn) return;

    document.querySelectorAll(".cat").forEach(b => {
        b.classList.remove("active");
    });

    btn.classList.add("active");

    category = btn.dataset.cat;
    filter();
});

/* ================= FILTER ================= */
function filter() {

    const cards = getCards();

    cards.forEach(c => {

        const okStatus =
            status === "all" || c.dataset.status === status;

        const okCat =
            category === "all" || c.dataset.cat === category;

        c.style.display = (okStatus && okCat) ? "block" : "none";
    });
}

/* ================= OPEN DETAIL ================= */
document.addEventListener("click", function (e) {

    const card = e.target.closest(".card");
    if (!card) return;

    currentProjectId = card.dataset.projectId;

    const grid = document.getElementById("grid");
    const detail = document.getElementById("detail");

    if (!grid || !detail) return;

    grid.style.display = "none";
    detail.classList.add("active");

    /* ================= BASIC INFO ================= */
    const img = document.getElementById("img");
    const title = document.getElementById("title");
    const client = document.getElementById("client");
    const date = document.getElementById("date");
    const desc = document.getElementById("desc");

    if (img) img.src = card.dataset.img || "";
    if (title) title.textContent = card.dataset.title || "";
    if (client) client.textContent = card.dataset.client || "";
    if (date) date.textContent = card.dataset.date || "";
    if (desc) desc.textContent = card.dataset.desc || "";

    /* ================= CATEGORY / SUBCATEGORY ================= */
    const categoryEl = document.getElementById("category");
    const subcategoryEl = document.getElementById("subcategory");

    if (categoryEl) categoryEl.textContent = card.dataset.category || "";
    if (subcategoryEl) subcategoryEl.textContent = card.dataset.subcategory || "";

    /* ================= GALLERY SWITCH ================= */
    showGallery(card.dataset.projectId);
});

/* ================= SHOW GALLERY ================= */
function showGallery(projectId) {

    const sets = document.querySelectorAll(".gallery-set");

    sets.forEach(set => {

        if (set.dataset.gallery === projectId) {
            set.style.display = "flex";
        } else {
            set.style.display = "none";
        }
    });
}

/* ================= BACK ================= */
function back() {

    const grid = document.getElementById("grid");
    const detail = document.getElementById("detail");

    if (!grid || !detail) return;

    detail.classList.remove("active");
    grid.style.display = "grid";

    currentProjectId = null;
}