# Telegram Secure Bridge Bot


Use this bot as an intermediate to communicate anonymously in groups.

### Setup instructions

#### 0. Setup virtualenv (recommended)

Install virtualenv with `pip install virtualenv`

```bash
virtualenv venv && cd venv
source bin/activate  # For linux

Scripts\activate # For Windows
```

#### 1. Clone repo and install requirements

```bash
git clone https://github.com/nikochiko/tg-securebridge.git
cd tg-securebridge

pip install -r requirements.txt
```

#### 2. Grab your bot token from [@Botfather](https://t.me/@BotFather) on telegram

Use `/newbot` command and follow setup instructions.

Then rename the `.env.example` file to `.env` and paste your telegram token
in `TELEGRAM_BOT_TOKEN=$right_here`.

#### 3. Run the bot

From inside the virtualenv, run:

```bash
python bot.py
```
