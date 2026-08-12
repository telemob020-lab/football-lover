from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.config import CHANNEL_URL
from app.database import (
    create_or_update_user,
    set_language,
    save_result,
    get_user,
)
from app.keyboards import (
    language_keyboard,
    start_quiz_keyboard,
    question_keyboard,
    channel_keyboard,
)
from app.questions import QUESTIONS


router = Router()

quiz_sessions = {}


TEXTS = {
    "en": {
        "choose_language": "⚽ <b>Choose your language</b>",
        "intro": (
            "⚽ <b>Think you know football? 🧠</b>\n\n"
            "Prove it and discover your <b>Football IQ</b>.\n\n"
            "🎯 <b>5 questions.</b>\n"
            "🔥 One chance to prove your knowledge.\n"
            "🏆 Your answers determine your Football IQ."
        ),
        "result": (
            "🧠 <b>YOUR FOOTBALL IQ</b>\n\n"
            "<b>{iq} IQ</b>\n\n"
            "🏆 <b>{rank}</b>\n\n"
            "🎯 {correct}/5 Correct\n"
            "📊 Accuracy: {accuracy}%"
        ),
        "join": (
            "⚽ <b>Want to join other football lovers?</b>\n\n"
            "Join our Football Lovers channel and stay connected "
            "with the community. ❤️⚽"
        ),
    },

    "ar": {
        "choose_language": "⚽ <b>اختر لغتك</b>",
        "intro": (
            "⚽ <b>تعتقد إنك فاهم في كرة القدم؟ 🧠</b>\n\n"
            "أثبت معرفتك واكتشف مستوى <b>Football IQ</b> الخاص بك.\n\n"
            "🎯 <b>5 أسئلة فقط.</b>\n"
            "🔥 فرصة واحدة لإثبات معرفتك.\n"
            "🏆 إجاباتك هي التي تحدد مستوى Football IQ الخاص بك."
        ),
        "result": (
            "🧠 <b>مستوى Football IQ الخاص بك</b>\n\n"
            "<b>{iq} IQ</b>\n\n"
            "🏆 <b>{rank}</b>\n\n"
            "🎯 {correct}/5 إجابات صحيحة\n"
            "📊 الدقة: {accuracy}%"
        ),
        "join": (
            "⚽ <b>عايز تنضم لعشاق كرة القدم؟</b>\n\n"
            "انضم إلى قناة Football Lovers وكن جزءًا من مجتمع "
            "عشاق كرة القدم. ❤️⚽"
        ),
    },
}


def get_text(language: str, key: str):
    return TEXTS.get(language, TEXTS["en"]).get(key, "")


def get_rank(iq: int):
    if iq >= 1000:
        return "🐐 Football Legend"
    if iq >= 800:
        return "👑 Football Master"
    if iq >= 600:
        return "🧠 Football Expert"
    if iq >= 400:
        return "🔥 Football Enthusiast"
    if iq >= 200:
        return "⚽ Football Fan"

    return "🥅 Casual Fan"


@router.message(CommandStart())
async def start(message: Message):
    await create_or_update_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        get_text("en", "choose_language"),
        reply_markup=language_keyboard()
    )


@router.callback_query(F.data.startswith("lang:"))
async def select_language(callback: CallbackQuery):
    language = callback.data.split(":")[1]

    await set_language(callback.from_user.id, language)

    await callback.message.edit_text(
        get_text(language, "intro"),
        reply_markup=start_quiz_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery):
    user_id = callback.from_user.id

    quiz_sessions[user_id] = {
        "question": 0,
        "iq": 0,
        "correct": 0,
    }

    await send_question(callback.message, user_id)

    await callback.answer()


async def send_question(message: Message, user_id: int):
    session = quiz_sessions[user_id]
    index = session["question"]
    question = QUESTIONS[index]

    await message.edit_text(
        f"🧠 <b>Question {index + 1}/5</b>\n\n"
        f"{question['question']}",
        reply_markup=question_keyboard(
            index,
            question["options"]
        )
    )


@router.callback_query(F.data.startswith("answer:"))
async def answer_question(callback: CallbackQuery):
    _, question_index, answer_index = callback.data.split(":")

    question_index = int(question_index)
    answer_index = int(answer_index)

    user_id = callback.from_user.id
    session = quiz_sessions.get(user_id)

    if not session:
        await callback.answer(
            "Please start a new challenge.",
            show_alert=True
        )
        return

    question = QUESTIONS[question_index]

    if answer_index == question["correct"]:
        session["correct"] += 1
        session["iq"] += question["points"]
        feedback = "✅ Correct!"
    else:
        feedback = "❌ Wrong!"

    await callback.answer(feedback)

    session["question"] += 1

    if session["question"] >= 5:
        await finish_quiz(callback.message, user_id)
        return

    await send_question(callback.message, user_id)


async def finish_quiz(message: Message, user_id: int):
    session = quiz_sessions[user_id]

    iq = session["iq"]
    correct = session["correct"]
    accuracy = round((correct / 5) * 100)

    rank = get_rank(iq)

    user = await get_user(user_id)
    language = user[2] if user else "en"

    await save_result(
        user_id,
        iq,
        5,
        correct
    )

    await message.edit_text(
        get_text(language, "result").format(
            iq=iq,
            rank=rank,
            correct=correct,
            accuracy=accuracy
        )
    )

    await message.answer(
        get_text(language, "join"),
        reply_markup=channel_keyboard(CHANNEL_URL)
    )

    quiz_sessions.pop(user_id, None)


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)

    if not user:
        await callback.answer(
            "Please use /start first.",
            show_alert=True
        )
        return

    user_id, username, language, iq, questions, correct = user

    accuracy = (
        round((correct / questions) * 100)
        if questions
        else 0
    )

    rank = get_rank(iq)

    text = (
        "⚽ <b>FOOTBALL LOVERS</b>\n\n"
        f"👤 @{username or 'Player'}\n\n"
        f"🧠 Football IQ: <b>{iq}</b>\n"
        f"🏆 Rank: <b>{rank}</b>\n"
        f"🎯 Questions: <b>{questions}</b>\n"
        f"✅ Correct: <b>{correct}</b>\n"
        f"📊 Accuracy: <b>{accuracy}%</b>"
    )

    await callback.message.edit_text(text)
    await callback.answer()
