document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contactForm");
    const success = document.getElementById("successMessage");
    const submitBtn = form ? form.querySelector('button[type="submit"]') : null;

    if (!form) return;

    const fields = {
        name: document.getElementById("name"),
        email: document.getElementById("email"),
        phone: document.getElementById("phone"),
        message: document.getElementById("message"),
        full_name: document.getElementById("full_name"),
        email_address: document.getElementById("email_address"),
        phone_number: document.getElementById("phone_number"),
        project_details: document.getElementById("project_details"),
        project: document.getElementById("project"),
        lead_type: document.getElementById("lead_type"),
        source: document.getElementById("source"),
    };

    function syncHiddenFields() {
        if (fields.full_name && fields.name) fields.full_name.value = fields.name.value || "";
        if (fields.email_address && fields.email) fields.email_address.value = fields.email.value || "";
        if (fields.phone_number && fields.phone) fields.phone_number.value = fields.phone.value || "";
        if (fields.project_details && fields.message) fields.project_details.value = fields.message.value || "";

        if (fields.project && !fields.project.value) fields.project.value = "Contact Inquiry";
        if (fields.lead_type && !fields.lead_type.value) fields.lead_type.value = "contact";
        if (fields.source && !fields.source.value) fields.source.value = "contact";
    }

    function showSuccessMessage(text) {
        if (!success) return;
        if (text) success.textContent = text;
        success.classList.add("show");

        setTimeout(() => {
            success.classList.remove("show");
        }, 4000);
    }

    function setSubmitting(isSubmitting) {
        if (!submitBtn) return;
        submitBtn.disabled = isSubmitting;
        submitBtn.style.opacity = isSubmitting ? "0.7" : "";
        submitBtn.style.pointerEvents = isSubmitting ? "none" : "";
    }

    async function submitContactForm() {
        syncHiddenFields();

        const actionUrl = form.getAttribute("action") || window.location.href;
        const csrfInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
        const csrfToken = csrfInput ? csrfInput.value : "";

        const formData = new FormData(form);
        const payload = new URLSearchParams();

        for (const [key, value] of formData.entries()) {
            if (typeof value === "string") {
                payload.append(key, value);
            }
        }

        const response = await fetch(actionUrl, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json, text/html;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
            },
            body: payload.toString(),
        });

        const contentType = response.headers.get("content-type") || "";
        let data = null;

        if (contentType.includes("application/json")) {
            try {
                data = await response.json();
            } catch (error) {
                data = null;
            }
        }

        if (!response.ok) {
            const message =
                (data && (data.message || data.error)) ||
                "Something went wrong. Please try again.";
            throw new Error(message);
        }

        form.reset();
        syncHiddenFields();

        const message =
            (data && (data.message || data.status)) ||
            "Thank you. Your message has been received.";

        showSuccessMessage(message);
    }

    ["input", "change", "blur"].forEach(function (eventName) {
        if (fields.name) fields.name.addEventListener(eventName, syncHiddenFields);
        if (fields.email) fields.email.addEventListener(eventName, syncHiddenFields);
        if (fields.phone) fields.phone.addEventListener(eventName, syncHiddenFields);
        if (fields.message) fields.message.addEventListener(eventName, syncHiddenFields);
    });

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        try {
            setSubmitting(true);
            await submitContactForm();
        } catch (error) {
            showSuccessMessage(error.message || "Submission failed.");
        } finally {
            setSubmitting(false);
        }
    });

    syncHiddenFields();
});