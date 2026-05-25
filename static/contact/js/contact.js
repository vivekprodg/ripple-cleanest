document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contactForm');
    const success = document.getElementById('successMessage');

    if (!form || !success) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // show success message
        success.classList.add('show');

        // reset form fields
        form.reset();

        // hide success message after 4 seconds
        setTimeout(() => {
            success.classList.remove('show');
        }, 4000);
    });
});