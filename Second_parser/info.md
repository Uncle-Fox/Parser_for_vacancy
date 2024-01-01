# Парсер

В данной папке находится второй "парсер", который более тонко настроен на поиск необходимых вакансий.

- Язык реализации: **Python**
- Вспомогательная библиотека: **Requests**, **BeautifulSoup**, **lxml**, **fake_useragent** (если не использовали ранее, то требуется установка)
- Тестовая страница для парсинга: *<https://hh.ru/search/vacancy?text=программист+Python&salary=&ored_clusters=true&page=1>*

---

#### Обнаружились проблемы:

1) При отсечке в 2 секунды, сайт выдает только 80 вакансий, при их наличии в >1000.
- Парсинг динамических данных: внизу страницы всегда отображается одинаковое кол-во страниц, однако в них меняются ссылки. 

Результат: