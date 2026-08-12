import aiosqlite

DB_PATH = "football_lovers.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                language TEXT,
                football_iq INTEGER DEFAULT 0,
                questions_answered INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0
            )
        """)
        await db.commit()


async def create_or_update_user(user_id: int, username: str | None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, username)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET username = excluded.username
        """, (user_id, username))

        await db.commit()


async def set_language(user_id: int, language: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?",
            (language, user_id)
        )
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return await cursor.fetchone()


async def save_result(
    user_id: int,
    football_iq: int,
    questions_answered: int,
    correct_answers: int,
):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users
            SET football_iq = ?,
                questions_answered = questions_answered + ?,
                correct_answers = correct_answers + ?
            WHERE user_id = ?
        """, (
            football_iq,
            questions_answered,
            correct_answers,
            user_id
        ))

        await db.commit()
