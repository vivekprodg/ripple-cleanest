/* =========================================
   Ripple Cleanest - WhatsApp Floating Button
   JS (Dynamic Link + Device Detection)
   ========================================= */

document.addEventListener("DOMContentLoaded", function () {
    // ==============================
    // GET CMS VALUES FROM TEMPLATE
    // ==============================
    const phoneNumber = (window.WHATSAPP_PHONE_NUMBER || "").trim();
    const preFilledText = (window.WHATSAPP_PREFILLED_TEXT || "").trim();
    const isActive = String(window.WHATSAPP_IS_ACTIVE).toLowerCase() === "true";

    // ==============================
    // BUTTON ELEMENT
    // ==============================
    const whatsappBtn = document.getElementById("whatsappLink");
    const whatsappContainer = document.querySelector(".whatsapp-btn-container");

    if (!whatsappBtn || !whatsappContainer) return;

    // ==============================
    // HIDE IF DISABLED OR NO NUMBER
    // ==============================
    if (!isActive || !phoneNumber) {
        whatsappContainer.style.display = "none";
        return;
    }

    // ==============================
    // ENCODE MESSAGE
    // ==============================
    const encodedText = encodeURIComponent(preFilledText || "Hello! I would like to get more information about your services.");

    // ==============================
    // DEVICE DETECTION
    // ==============================
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
    );

    // ==============================
    // BASE URL SELECTION
    // ==============================
    const baseUrl = isMobile
        ? "https://api.whatsapp.com/send"
        : "https://web.whatsapp.com/send";

    // ==============================
    // FINAL URL
    // ==============================
    const finalUrl = `${baseUrl}?phone=${phoneNumber}&text=${encodedText}`;

    // ==============================
    // APPLY TO BUTTON
    // ==============================
    whatsappBtn.href = finalUrl;
});