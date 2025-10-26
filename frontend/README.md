## Фронтенд-стэк

- Typescript
- React 19
- Redux Toolkit: упраление состоянием
- React Router: клиентский роутинг
- React Hook Form: формы
- Vite
- shadcn/ui с Tailwind СSS
- см. другие зависимости в [`package.json`](package.json)

## Методологии и соглашения

<!-- - [FSD](https://feature-sliced.design/ru/) -->
<!-- - [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) -->

- Названия веток в git: `[type]/[short-description]`, возможные типы:

  - `feat` добавляет функциональность для конечного пользователя
  - `refactor` изменения в коде приложения, не добавляющие функциональность и не исправляющие баги
  - `bugfix`
  - `chore` изменения, не влияющие на код приложения (зависимости/конфиги/CI/скрипты и пр.)
  - `docs`

- mobile first верстка.

## Как запустить

```sh
git clone https://github.com/Hexlet/hexlet-price-tracker.git
cd hexlet-price-tracker/frontend/
code .
npm i
npm run dev
```

## Как сделать сборку

```sh
npm run build
```

P.S. Вы должны находиться в папке frontend

см. другие скрипты в [`package.json`](package.json)