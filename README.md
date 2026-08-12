# ⚽ Football Lovers Bot

Football Lovers is a Telegram football quiz bot where users test their football knowledge, earn Football IQ, and compete to become a Football Legend.

## 🎯 Current Features

- 🌍 7 language selection
- 🧠 Football IQ challenge
- 🎯 5 questions per challenge
- 📊 Accuracy tracking
- 🏆 Football ranks
- 👤 User profile
- ⚽ Football Lovers channel integration
- 💾 SQLite database
- 🐍 Python + aiogram 3.x
- 🚂 Railway-ready deployment

## 🌍 Supported Languages

- 🇬🇧 English
- 🇪🇸 Español
- 🇸🇦 العربية
- 🇫🇷 Français
- 🇩🇪 Deutsch
- 🇮🇹 Italiano
- 🇵🇹 Português

## 🧠 Football IQ Ranks

| Football IQ | Rank |
|---:|---|
| 0–199 | 🥅 Casual Fan |
| 200–399 | ⚽ Football Fan |
| 400–599 | 🔥 Football Enthusiast |
| 600–799 | 🧠 Football Expert |
| 800–999 | 👑 Football Master |
| 1000+ | 🐐 Football Legend |

## 🛠️ Tech Stack

- Python
- aiogram 3.x
- SQLite
- aiosqlite
- python-dotenv

## ⚙️ Environment Variables

Create a `.env` file locally:

BOT_TOKEN=YOUR_BOT_TOKEN
CHANNEL_URL=https://t.me/YOUR_CHANNEL

Never commit your `.env` file or bot token to GitHub.

## 🚀 Run Locally

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the bot:

python -m app.bot

## 🚂 Railway Deployment

Add the following environment variables to Railway:

BOT_TOKEN
CHANNEL_URL

Then deploy the project.

## 📁 Project Structure

football-lovers-bot/

├── app/
│   ├── __init__.py
│   ├── bot.py
│   ├── config.py
│   ├── database.py
│   ├── keyboards.py
│   ├── questions.py
│   └── handlers.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── Procfile
└── README.md

## 🔮 Planned Features

- 🔥 Daily Challenge
- 📈 IQ Progress
- 🏆 Global Leaderboard
- 👥 Group Leaderboard
- 🔥 Streaks
- 🎖️ Badges
- ⚔️ 1v1 Challenges
- 🧩 Guess the Player
- 🔥 Football Debates
- 🎁 Achievements
