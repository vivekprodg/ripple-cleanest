/* =========================================
   BLOG FILTERS
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    const filterButtons = document.querySelectorAll(
        ".blog-filters button"
    );

    if (!filterButtons.length) return;

    filterButtons.forEach(button => {

        button.addEventListener("click", () => {

            // REMOVE ACTIVE STATE
            filterButtons.forEach(btn => {
                btn.classList.remove("active");
            });

            // ADD ACTIVE STATE
            button.classList.add("active");

            // CURRENT FILTER
            const currentFilter = button.dataset.filter;

            // FUTURE DJANGO / AJAX FILTER HOOK
            console.log("Current Filter:", currentFilter);

        });

    });

});