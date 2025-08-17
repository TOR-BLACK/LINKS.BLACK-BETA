## Запуск проекта

### Запуск dev сервера

1. Установить зависимости:

```bash
npm i
# or
yarn
```

2. Запуск сервера:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

### Запуск production сервера:

1. Установить зависимости

```bash
npm i
# or
yarn
```

1. Сборка прокета

```bash
npm run build
# or
yarn build
# or
pnpm build
# or
bun build
```

2. Запуск проекта

```bash
npm run start
# or
yarn start
# or
pnpm start
# or
bun start
```

## Выжные дополнения

1. Для корректной работы переменных окружения важно создать файл `.env`, который нужно заполнить по аналогии `.env.example`.

Например:

```env
NEXT_PUBLIC_API_BASE_URL=https://localhost/api/v1/dvi
```

2. Для оптимизации картинок заполнить файл `next.config.mjs` в котором в строке изменить hostname на корректный:

```js
  images: {
    remotePatterns: [
      {
        hostname: "localhost", // Здесь изменить имя хоста с которого грузятся картинки
      },
    ],
  },
```

## Инструкция по локализации

Для локализации вам нужно заполнить файлы `.json`, находящиеся в `src/messages`. Заполнять нужно по примеру русской локали (файлик `ru.json`).

Если вы не знаете за что отвечает конкретный ключ, вы можете оставить его пустым - в результате вы увидите какое именно свойство не заполнено зайдя на страницу.

> Пример:
>
> ```
>   "Header": {
>     ///
>    "headerNav": {
>      ///
>      "telegramButton": ""
> ```
>
> Поле telegramButton не заполнено
>
> Тогда на странице в тексте этого элемента вы увидите - Header.headerNav.telegramButton
