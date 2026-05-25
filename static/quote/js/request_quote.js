/* =========================================================
   REQUEST FOR QUOTE (RFQ) PAGE SCRIPT
   Ripple Cleanest Architecture System
   PRO SYSTEM: AJAX submission + loading + success/error + anti-spam
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("comprehensive-rfq");
    const submitBtn = document.getElementById("submit-brief");
    const successScreen = document.getElementById("success-screen");

    if (!form || !submitBtn || !successScreen) return;

    const emailRegex = /^\S+@\S+\.\S+$/;
    const submitUrl = form.getAttribute("action") || window.location.href;
    const pageLoadedAt = Date.now();
    const MIN_FILL_TIME_MS = 2500;

    let isSubmitting = false;

    function getCsrfToken() {
        const csrfInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput && csrfInput.value) return csrfInput.value;

        const cookieMatch = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
        return cookieMatch ? decodeURIComponent(cookieMatch[1]) : "";
    }

    function ensureStatusBox() {
        let box = document.getElementById("rfq-status-box");
        if (!box) {
            box = document.createElement("div");
            box.id = "rfq-status-box";
            box.setAttribute("role", "status");
            box.setAttribute("aria-live", "polite");
            box.style.margin = "0 0 16px 0";
            box.style.padding = "12px 14px";
            box.style.borderRadius = "10px";
            box.style.fontSize = "14px";
            box.style.lineHeight = "1.5";
            box.style.display = "none";

            form.parentNode.insertBefore(box, form);
        }
        return box;
    }

    function showStatus(message, type) {
        const box = ensureStatusBox();
        box.textContent = message;
        box.style.display = "block";

        if (type === "success") {
            box.style.background = "#ecfdf5";
            box.style.color = "#065f46";
            box.style.border = "1px solid #a7f3d0";
        } else if (type === "error") {
            box.style.background = "#fef2f2";
            box.style.color = "#991b1b";
            box.style.border = "1px solid #fecaca";
        } else {
            box.style.background = "#eff6ff";
            box.style.color = "#1d4ed8";
            box.style.border = "1px solid #bfdbfe";
        }
    }

    function hideStatus() {
        const box = document.getElementById("rfq-status-box");
        if (box) box.style.display = "none";
    }

    function setSubmittingState(submitting) {
        isSubmitting = submitting;

        if (submitting) {
            submitBtn.textContent = "Encrypting & Routing Brief...";
            submitBtn.disabled = true;
            submitBtn.style.opacity = "0.65";
            submitBtn.style.pointerEvents = "none";
            submitBtn.setAttribute("aria-busy", "true");
        } else {
            submitBtn.textContent = "Transmit Architecture Brief";
            submitBtn.disabled = false;
            submitBtn.style.opacity = "1";
            submitBtn.style.pointerEvents = "auto";
            submitBtn.removeAttribute("aria-busy");
        }
    }

    function validateField(field) {
        const group = field.closest(".field-group");
        if (!group) return true;

        const value = field.value ? field.value.trim() : "";
        let isValid = true;

        if (field.hasAttribute("required") && !value) {
            isValid = false;
        }

        if (field.type === "email" && value && !emailRegex.test(value)) {
            isValid = false;
        }

        if (isValid) {
            group.classList.remove("invalid");
        } else {
            group.classList.add("invalid");
        }

        return isValid;
    }

    function validateForm() {
        const requiredFields = form.querySelectorAll("input[required], select[required], textarea[required]");
        let isFormValid = true;

        requiredFields.forEach((field) => {
            const valid = validateField(field);
            if (!valid) isFormValid = false;
        });

        return isFormValid;
    }

    function antiSpamCheck() {
        const elapsed = Date.now() - pageLoadedAt;

        if (elapsed < MIN_FILL_TIME_MS) {
            return {
                ok: false,
                message: "Please take a moment to review the brief before submitting."
            };
        }

        const honeypot =
            form.querySelector('input[name="website"]') ||
            form.querySelector('input[name="company_website"]') ||
            form.querySelector('input[name="url"]');

        if (honeypot && honeypot.value && honeypot.value.trim() !== "") {
            return {
                ok: false,
                message: "Submission blocked."
            };
        }

        return { ok: true };
    }

    function clearInvalidStates() {
        const invalidGroups = form.querySelectorAll(".field-group.invalid");
        invalidGroups.forEach((group) => group.classList.remove("invalid"));
    }

    function scrollToTopSmooth() {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }

    async function submitFormAjax() {
        const csrfToken = getCsrfToken();
        const formData = new FormData(form);

        const response = await fetch(submitUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json"
            },
            body: formData
        });

        const contentType = response.headers.get("content-type") || "";
        let data = null;

        if (contentType.includes("application/json")) {
            data = await response.json();
        } else {
            const text = await response.text();
            data = {
                success: false,
                message: text || "Unexpected server response."
            };
        }

        if (!response.ok) {
            const message =
                (data && (data.message || data.error)) ||
                "We could not submit your brief. Please try again.";
            throw new Error(message);
        }

        return data;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (isSubmitting) return;

        hideStatus();
        clearInvalidStates();

        const isValid = validateForm();
        if (!isValid) {
            showStatus("Please complete the required fields correctly.", "error");
            return;
        }

        const antiSpam = antiSpamCheck();
        if (!antiSpam.ok) {
            showStatus(antiSpam.message, "error");
            return;
        }

        setSubmittingState(true);
        showStatus("Submitting your architecture brief...", "info");

        try {
            const data = await submitFormAjax();

            showStatus(
                data.message || "Your brief has been received successfully.",
                "success"
            );

            form.reset();
            scrollToTopSmooth();

            setTimeout(() => {
                successScreen.classList.add("active");
            }, 250);
        } catch (error) {
            showStatus(
                error.message || "Submission failed. Please try again.",
                "error"
            );
        } finally {
            setSubmittingState(false);
        }
    });

    const inputs = form.querySelectorAll(".field-input");

    inputs.forEach((input) => {
        input.addEventListener("input", () => {
            const group = input.closest(".field-group");
            if (group) group.classList.remove("invalid");
        });

        input.addEventListener("change", () => {
            validateField(input);
        });

        input.addEventListener("blur", () => {
            validateField(input);
        });
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            successScreen.classList.remove("active");
            hideStatus();
            setSubmittingState(false);
        }
    });
});