document.addEventListener('DOMContentLoaded', () => {

    const cards = document.querySelectorAll('.member-card');
    const teamStrip = document.getElementById('teamStrip');

    if (!teamStrip || !cards.length) return;

    const observer = new IntersectionObserver((entries) => {

        if (entries[0].isIntersecting) {

            cards.forEach((card, index) => {

                setTimeout(() => {

                    card.style.transition =
                        'all 0.8s cubic-bezier(0.19, 1, 0.22, 1)';

                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';

                }, index * 80);

            });

            observer.unobserve(teamStrip);
        }

    }, {
        threshold: 0.2
    });

    observer.observe(teamStrip);

});