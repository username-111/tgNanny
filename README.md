# tgNanny (Telegram webcam bot)

Бот по команде `/snap` делает снимок с веб-камеры и отправляет его в Telegram только разрешённому пользователю.
Также доступна команда `/shutdown` — выключение компьютера (Windows) через 30 секунд.

## 1) Получить токен Telegram-бота

1. Откройте Telegram и найдите бота **@BotFather**.
2. Отправьте команду `/newbot`.
3. Задайте имя и username для бота.
4. Скопируйте выданный токен (строка вида `123456789:AA...`).

## 2) Узнать `allowed_user_id`

Есть несколько способов:

- написать боту **@userinfobot** и взять поле `Id`;
- либо отправить сообщение вашему боту, временно вывести `message.from_user.id` в обработчике и посмотреть значение в консоли.

В `allowed_user_id` нужен **числовой** Telegram ID вашего аккаунта.

## 3) Настроить конфиг

1. Скопируйте файл `config.example.ini` в `config.ini`.
2. Заполните реальные значения:

```ini
[telegram]
bot_token = 123456789:AA...
allowed_user_id = 123456789
```

`config.ini` добавлен в `.gitignore`, поэтому реальные токены не попадут в Git.

## 4) Создать виртуальное окружение и установить зависимости

Из корня проекта:

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Если политика выполнения блокирует активацию:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 5) Запуск бота

В активированном виртуальном окружении:

```bash
python cam_bot.py
```

Или на Windows можно запустить готовый файл:

```bat
run_bot.bat
```

Он автоматически:
- создаст `.venv` (если её ещё нет);
- установит зависимости из `requirements.txt`;
- запустит бота.

Если всё настроено правильно, в консоли появится:

`Бот запущен. Нажмите Ctrl+C для остановки.`

После этого в Telegram отправьте боту команду `/snap`.

## 6) Команды бота

- `/snap` — сделать фото с веб-камеры;
- `/shutdown` — выключить компьютер через 30 секунд (только для `allowed_user_id`).

Для отмены отложенного выключения в Windows можно выполнить локально:

```bat
shutdown /a
```
