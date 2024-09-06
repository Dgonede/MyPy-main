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

document.querySelectorAll('.card-container').forEach(container => {
    const decreaseBtn = container.querySelector('#decrease');
    const increaseBtn = container.querySelector('#increase');
    const quantityInput = container.querySelector('.quantity-input');

    decreaseBtn.addEventListener('click', () => {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });

    increaseBtn.addEventListener('click', () => {
        let currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });

    // Обработка отправки формы
    const form = container.querySelector('.add-to-cart-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Отменяем стандартное поведение формы

            const url = form.getAttribute('data-url');
            const data = new URLSearchParams(new FormData(form)).toString(); // Собираем данные формы

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value // Добавляем CSRF токен
                },
                body: data
            })
            .then(response => {
                if (response.ok) {
                    return response.json(); // Возвращаем JSON-ответ
                } else {
                    throw new Error('Ошибка при добавлении товара в корзину.');
                }
            })
            .then(data => {
                // Обновляем счетчик в корзине
                const cartCountElement = document.querySelector('.cart-icon .badge');
                if (cartCountElement) {
                    cartCountElement.textContent = data.cart_item_count; // Обновляем текст счетчика
                } else {
                    // Если счетчик отсутствует, создаем его
                    const newBadge = document.createElement('span');
                    newBadge.className = 'badge bg-danger';
                    newBadge.textContent = data.cart_item_count;
                    document.querySelector('.cart-icon').appendChild(newBadge);
                }
                
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Ошибка при добавлении товара в корзину.');
            });
        });
    }
});


const checkoutForm = document.querySelector("form[action='{% url 'store_app:checkout' %}']");
if (checkoutForm) {
    checkoutForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Отменяем стандартное поведение формы

        const url = checkoutForm.getAttribute('action');
        const data = new URLSearchParams(new FormData(checkoutForm)).toString(); // Собираем данные формы

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': checkoutForm.querySelector('[name=csrfmiddlewaretoken]').value // Добавляем CSRF токен
            },
            body: data
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Возвращаем JSON-ответ
            } else {
                throw new Error('Ошибка при оформлении заказа.');
            }
        })
        .then(data => {
            // Проверяем, есть ли сообщение в ответе
            if (data.message) {
                alert(data.message); // Показываем сообщение об успешном оформлении

                // Сбрасываем счетчик на иконке корзины
                const cartCountElement = document.querySelector('.cart-icon .badge');
                if (cartCountElement) {
                    cartCountElement.textContent = '0'; // Устанавливаем счетчик в 0
                } else {
                    // Если счетчика нет, можно создать его (если это необходимо)
                    const newBadge = document.createElement('span');
                    newBadge.className = 'badge bg-danger';
                    newBadge.textContent = '0';
                    document.querySelector('.cart-icon').appendChild(newBadge);
                }
            } else {
                alert('Не удалось получить сообщение об успешном оформлении.');
            }
            window.location.reload(); // Перезагружаем страницу, чтобы обновить корзину
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Ошибка при оформлении заказа.');
        });
    });
}


