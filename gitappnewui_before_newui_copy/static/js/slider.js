/**
 * Слайдер изображений — модуль 2.
 * Интервал задаётся data-interval на .hero-slider (из exam_config.py).
 */
document.addEventListener("DOMContentLoaded", () => {
    const slider = document.querySelector(".hero-slider");
    if (!slider) return;

    const slides = slider.querySelectorAll(".slider-slide");
    const prevBtn = slider.querySelector(".slider-btn.prev");
    const nextBtn = slider.querySelector(".slider-btn.next");
    if (!slides.length) return;

    let index = 0;
    const interval = parseInt(slider.dataset.interval || "3000", 10);
    let timer = null;

    function show(i) {
        slides.forEach((s, n) => s.classList.toggle("active", n === i));
        index = i;
    }

    function next() {
        show((index + 1) % slides.length);
    }

    function prev() {
        show((index - 1 + slides.length) % slides.length);
    }

    function startAuto() {
        stopAuto();
        timer = setInterval(next, interval);
    }

    function stopAuto() {
        if (timer) clearInterval(timer);
    }

    nextBtn?.addEventListener("click", () => { next(); startAuto(); });
    prevBtn?.addEventListener("click", () => { prev(); startAuto(); });

    startAuto();
});
