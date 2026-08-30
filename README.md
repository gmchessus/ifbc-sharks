# ИФБК «Акулы» — сайт клуба

Статический русскоязычный сайт флорбольного клуба ИФБК «Акулы» (Санкт-Петербург), собранный на **Hugo**.

- Публичный адрес: <https://gmchessus.duckdns.org>
- Индексация поисковиками запрещена (`robots.txt`, meta `noindex`, заголовок `X-Robots-Tag`).

## Технологии

- **Hugo** (см. `hugo.toml`) — генерация статики в каталог `public/`.
- Чистые HTML/CSS/JS без фреймворков; шрифты и дизайн — в `public/assets/styles.css`.
- Продакшен раздаётся **Caddy** из `public/` (активный конфиг вне репозитория: `/etc/caddy/sites/gmchessus.duckdns.org.caddy`).
- Полный runbook по развёртыванию и эксплуатации — в [README.cd](README.cd).

## Структура проекта

```text
.
├── hugo.toml                    # Конфигурация Hugo (baseURL, модули, outputs)
├── content/                     # Страницы и фотоальбомы в Markdown
│   ├── _index.md                # Главная
│   ├── about.md                 # О клубе
│   ├── team.md                  # Состав
│   ├── awards.md                # Зал наград
│   ├── young-team.md            # Детские команды
│   ├── photo.md                 # Фотогалерея (18 альбомов)
│   ├── video.md                 # Видео
│   ├── shop.md                  # Магазин
│   ├── rukovodstvo.md           # Руководство
│   ├── archive.md               # Медиаархив
│   └── photo/                   # Страницы отдельных альбомов
├── layouts/                     # Шаблоны Hugo
│   ├── 404.html                 # Страница «Страница не найдена»
│   ├── index.html               # Главная
│   ├── _default/                # baseof.html, single.html
│   ├── partials/                # header.html, footer.html, topstrip.html
│   ├── <раздел>/single.html     # Шаблоны разделов (about, photo, shop, …)
│   └── robots.txt               # Генерируется в public/robots.txt
├── static/                      # Статика, копируется в public/ как есть
│   ├── _headers                 # X-Robots-Tag для совместимых хостингов
│   ├── assets/                  # styles.css, nav.js
│   └── images/, photo/, shop/   # Изображения
├── data/photos/*.json           # Данные 18 фотоальбомов
├── archive/                     # Скачанный архив старого сайта (1041 фото)
│   ├── media/legacy/            # Фотографии с исходной структурой URL
│   ├── media-index.js           # Индекс фотографий
│   ├── archive.js               # Поиск, пагинация и lightbox
│   ├── photo-download-report.csv# Реестр скачанных фото
│   └── video-links.txt          # Ссылки на внешний видеоархив
├── public/                      # Собранный сайт (результат `hugo`)
├── scripts/inventory.py         # Read-only инвентаризация старого сайта
├── server/nginx-noindex.conf    # Справочный пример конфигурации Nginx
├── docs/                        # ТЗ и материалы по миграции архива
├── README.cd                    # Эксплуатация: Caddy, проверки, ограничения
└── index.html, archive.html     # Ранний статический прототип (в сборку не входит)
```

Каталог `archive/` подключён в сборку через module mount (`archive` → `static/archive`), поэтому его содержимое попадает в `public/archive/`.

## Локальная разработка

```bash
hugo server -D
# открыть http://localhost:1313
```

## Сборка

```bash
hugo
```

Результат — каталог `public/`, именно его раздаёт Caddy. Страница 404 собирается в `public/404.html` из `layouts/404.html`; на проде её отдаёт блок `handle_errors` в конфиге Caddy (см. README.cd).

## Контент

- **Страницы** — Markdown в `content/*.md` с front matter (`title`, `description`, `section`, `subtitle`).
- **Фотоальбомы** — альбомы описаны в `content/photo.md`, данные фотографий — в `data/photos/*.json`.
- **Награды, видео, товары** — данные в front matter страниц (`awards`, `videos`, `products`).
- **Архив** — 1041 фото и реестры в `archive/`; служебные заметки по переносу — `sitemap-ifbc-sharks.md`, `club-news-2023-2026.md`, `docs/archive-migration.md`.

## Важные ограничения

1. Не удалять `robots.txt`, meta-теги `noindex` и заголовок `X-Robots-Tag`.
2. Не заменять архивные материалы вымышленными фотографиями, датами или результатами матчей.
3. Перед изменением продакшена — следовать процедурам из [README.cd](README.cd) (валидация конфига Caddy, reload вместо restart, проверка соседних сайтов).
