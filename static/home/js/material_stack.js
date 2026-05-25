/**
 * =========================================================
 * MATERIAL STACK — INDEX SYNCHRONIZED CONTROLLER
 * =========================================================
 * Controls:
 * - Text blocks
 * - Image panels
 * - Index navigation
 *
 * STRICT RULE:
 * All arrays are CMS-synced by index:
 * text-block[i] ↔ image-panel[i] ↔ index-item[i]
 * =========================================================
 */

document.addEventListener("DOMContentLoaded", () => {

    const section = document.querySelector("#material-stack-section");

    if (!section) return;

    const textBlocks = Array.from(section.querySelectorAll(".text-block"));
    const imagePanels = Array.from(section.querySelectorAll(".image-panel"));
    const indexItems = Array.from(section.querySelectorAll(".index-item"));

    const count = Math.min(
        textBlocks.length,
        imagePanels.length,
        indexItems.length
    );

    if (count === 0) return;

    /**
     * CENTRAL STATE CONTROLLER
     */
    function setActive(index) {

        if (index < 0 || index >= count) return;

        // -------------------------
        // TEXT BLOCKS
        // -------------------------
        textBlocks.forEach((el, i) => {
            if (i === index) {
                el.classList.add("active");
            } else {
                el.classList.remove("active");
            }
        });

        // -------------------------
        // IMAGE PANELS
        // -------------------------
        imagePanels.forEach((el, i) => {
            if (i === index) {
                el.classList.add("active");
            } else {
                el.classList.remove("active");
            }
        });

        // -------------------------
        // INDEX ITEMS
        // -------------------------
        indexItems.forEach((el, i) => {
            if (i === index) {
                el.classList.add("active");
            } else {
                el.classList.remove("active");
            }
        });
    }

    /**
     * INIT STATE (FIRST ITEM ACTIVE)
     */
    setActive(0);

    /**
     * CLICK HANDLERS — INDEX DRIVES ENTIRE SYSTEM
     */
    indexItems.forEach((item) => {

        item.addEventListener("click", () => {

            const targetIndex = parseInt(
                item.getAttribute("data-target"),
                10
            );

            if (isNaN(targetIndex)) return;

            setActive(targetIndex);
        });

    });

});