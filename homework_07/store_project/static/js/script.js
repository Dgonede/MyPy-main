document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const cardRect = card.getBoundingClientRect();
        const x = e.clientX - cardRect.left; // Положение курсора относительно карточки
        const y = e.clientY - cardRect.top;

        // Вычисляем смещение
        const xOffset = (x / cardRect.width - 0.5) * 20; // 20 - максимальное смещение по X
        const yOffset = (y / cardRect.height - 0.5) * 20; // 20 - максимальное смещение по Y

        // Применяем трансформацию
        card.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });

    card.addEventListener('mouseleave', () => {
        // Возвращаем карточку в исходное положение
        card.style.transform = 'translate(0, 0)';
    });
});