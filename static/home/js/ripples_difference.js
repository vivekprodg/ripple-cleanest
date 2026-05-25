document.addEventListener('DOMContentLoaded', () => {
    const section = document.querySelector('.features-section');
    if (!section) return;

    const learnMoreBtn = section.querySelector('.feature-actions .btn--primary');

    if (learnMoreBtn) {
        learnMoreBtn.addEventListener('click', (e) => {
            const href = learnMoreBtn.getAttribute('href');

            if (!href || href === '#') {
                e.preventDefault();
                window.location.href = '/about/';
            }
        });
    }
});