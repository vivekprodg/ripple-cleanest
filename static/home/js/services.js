document.addEventListener('DOMContentLoaded', () => {
    const section = document.querySelector('.services-section');
    if (!section) return;

    const serviceItems = section.querySelectorAll('.service-item');
    const visualImages = section.querySelectorAll('.visual-image');

    if (!serviceItems.length || !visualImages.length) return;

    const activateService = (index) => {
        serviceItems.forEach((item) => {
            item.classList.toggle('active', item.dataset.service === index);
        });

        visualImages.forEach((img) => {
            img.classList.toggle('active', img.dataset.service === index);
        });
    };

    serviceItems.forEach((item) => {
        const index = item.dataset.service;

        item.addEventListener('mouseenter', () => {
            activateService(index);
        });

        item.addEventListener('click', () => {
            activateService(index);
        });
    });

    // initial state
    const first = section.querySelector('.service-item.active');
    if (first) activateService(first.dataset.service);
});