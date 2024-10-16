// Пример скрипта для улучшения пользовательского интерфейса
document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('table tbody tr');
    rows.forEach(row => {
        row.addEventListener('click', () => {
            window.location = row.querySelector('a').href; // Переход по клику на строку
        });
    });
});
