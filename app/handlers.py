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

        "question": "Question",

        "correct": "✅ Correct!",
        "wrong": "❌ Wrong!",

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

        "new_challenge": "Please start a new challenge.",
        "profile_error": "Please use /start first.",
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

        "question": "السؤال",

        "correct": "✅ إجابة صحيحة!",
        "wrong": "❌ إجابة خاطئة!",

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

        "new_challenge": "من فضلك ابدأ تحديًا جديدًا.",
        "profile_error": "من فضلك استخدم /start أولًا.",
    },

    "es": {
        "choose_language": "⚽ <b>Elige tu idioma</b>",

        "intro": (
            "⚽ <b>¿Crees que sabes de fútbol? 🧠</b>\n\n"
            "Demuéstralo y descubre tu <b>Football IQ</b>.\n\n"
            "🎯 <b>5 preguntas.</b>\n"
            "🔥 Una oportunidad para demostrar tus conocimientos.\n"
            "🏆 Tus respuestas determinarán tu Football IQ."
        ),

        "question": "Pregunta",

        "correct": "✅ ¡Correcto!",
        "wrong": "❌ ¡Incorrecto!",

        "result": (
            "🧠 <b>TU FOOTBALL IQ</b>\n\n"
            "<b>{iq} IQ</b>\n\n"
            "🏆 <b>{rank}</b>\n\n"
            "🎯 {correct}/5 Correctas\n"
            "📊 Precisión: {accuracy}%"
        ),

        "join": (
            "⚽ <b>¿Quieres unirte a otros amantes del fútbol?</b>\n\n"
            "Únete a nuestro canal Football Lovers y forma parte "
            "de nuestra comunidad. ❤️⚽"
        ),

        "new_challenge": "Por favor, comienza un nuevo desafío.",
        "profile_error": "Por favor, usa /start primero.",
    },

    "fr": {
        "choose_language": "⚽ <b>Choisissez votre langue</b>",

        "intro": (
            "⚽ <b>Vous pensez connaître le football ? 🧠</b>\n\n"
            "Prouvez-le et découvrez votre <b>Football IQ</b>.\n\n"
            "🎯 <b>5 questions.</b>\n"
            "🔥 Une chance de prouver vos connaissances.\n"
            "🏆 Vos réponses détermineront votre Football IQ."
        ),

        "question": "Question",

        "correct": "✅ Correct !",
        "wrong": "❌ Incorrect !",

        "result": (
            "🧠 <b>VOTRE FOOTBALL IQ</b>\n\n"
            "<b>{iq} IQ</b>\n\n"
            "🏆 <b>{rank}</b>\n\n"
            "🎯 {correct}/5 Correctes\n"
            "📊 Précision : {accuracy}%"
        ),

        "join": (
            "⚽ <b>Vous voulez rejoindre d'autres passionnés de football ?</b>\n\n"
            "Rejoignez notre canal Football Lovers et faites partie "
            "de notre communauté. ❤️⚽"
        ),

        "new_challenge": "Veuillez commencer un nouveau défi.",
        "profile_error": "Veuillez utiliser /start d'abord.",
    },

    "de": {
        "choose_language": "⚽ <b>Wähle deine Sprache</b>",

        "intro": (
            "⚽ <b>Du denkst, du kennst dich mit Fußball aus? 🧠</b>\n\n"
            "Beweise es und entdecke deinen <b>Football IQ</b>.\n\n"
            "🎯 <b>5 Fragen.</b>\n"
            "🔥 Eine Chance, dein Wissen zu beweisen.\n"
            "🏆 Deine Antworten bestimmen deinen Football IQ."
        ),

        "question": "Frage",

        "correct": "✅ Richtig!",
        "wrong": "❌ Falsch!",

        "result": (
            "🧠 <b>DEIN FOOTBALL IQ</b>\n\n"
            "<b>{iq} IQ</b>\n\n"
            "🏆 <b>{rank}</b>\n\n"
            "🎯 {correct}/5 Richtig\n"
            "📊 Genauigkeit: {accuracy}%"
        ),

        "join": (
            "⚽ <b>Möchtest du anderen Fußballfans beitreten?</b>\n\n"
            "Tritt unserem Football Lovers Kanal bei und werde Teil "
            "unserer Community. ❤️⚽"
        ),

        "new_challenge": "Bitte starte eine neue Herausforderung.",
        "profile_error": "Bitte benutze zuerst /start.",
    },

    "it": {
        "choose_language": "⚽ <b>Scegli la tua lingua</b>",

        "intro": (
            "⚽ <b>Pensi di conoscere il calcio? 🧠</b>\n\n"
            "Dimostralo e scopri il tuo <b>Football IQ</b>.\n\n"
            "🎯 <b>5 domande.</b>\n"
            "🔥 Un'occasione per dimostrare le tue conoscenze.\n"
            "🏆 Le tue risposte determineranno il tuo Football IQ."
        ),

        "question": "Domanda",

        "correct": "✅ Corretto!",
        "wrong": "❌ Sbagliato!",

        "result": (
            "🧠 <b>IL TUO FOOTBALL IQ</b>\n\n"
            "<b>{iq} IQ</b>\n\n"
            "🏆 <b>{rank}</b>\n\n"
            "🎯 {correct}/5 Corrette\n"
            "📊 Precisione: {accuracy}%"
        ),

        "join": (
            "⚽ <b>Vuoi unirti ad altri appassionati di calcio?</b>\n\n"
            "Unisciti al nostro canale Football Lovers e fai parte "
            "della nostra community. ❤️⚽"
        ),

        "new_challenge": "Inizia una nuova sfida.",
        "profile_error": "Usa prima /start.",
    },

    "pt": {
        "choose_language": "⚽ <b>Escolha seu idioma</b>",

        "intro": (
            "⚽ <b>Acha que entende de futebol? 🧠</b>\n\n"
            "Prove e descubra seu <b>Football IQ</b>.\n\n"
            "🎯 <b>5 perguntas.</b>\n"
            "🔥 Uma chance para provar seu conhecimento.\n"
            "🏆 Suas respostas determinarão seu Football IQ."
        ),

        "question": "Pergunta",

        "correct": "✅ Correto!",
        "wrong": "❌ Errado!",

        "result": (
            "🧠 <b>SEU FOOTBALL IQ</b>\n\n"
            "<b>{iq} IQ</b>\n\n"
            "🏆 <b>{rank}</b>\n\n"
            "🎯 {correct}/5 Corretas\n"
            "📊 Precisão: {accuracy}%"
        ),

        "join": (
            "⚽ <b>Quer se juntar a outros amantes do futebol?</b>\n\n"
            "Entre no nosso canal Football Lovers e faça parte "
            "da nossa comunidade. ❤️⚽"
        ),

        "new_challenge": "Por favor, comece um novo desafio.",
        "profile_error": "Por favor, use /start primeiro.",
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

    await set_language(
        callback.from_user.id,
        language
    )

    await callback.message.edit_text(
        get_text(language, "intro"),
        reply_markup=start_quiz_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery):
    user_id = callback.from_user.id

    user = await get_user(user_id)

    language = user[2] if user and user[2] else "en"

    quiz_sessions[user_id] = {
        "question": 0,
        "iq": 0,
        "correct": 0,
        "language": language,
    }

    await send_question(
        callback.message,
        user_id
    )

    await callback.answer()


async def send_question(message: Message, user_id: int):
    session = quiz_sessions[user_id]

    index = session["question"]
    language = session["language"]

    questions = QUESTIONS.get(
        language,
        QUESTIONS["en"]
    )

    question = questions[index]

    question_label = get_text(
        language,
        "question"
    )

    await message.edit_text(
        f"🧠 <b>{question_label} {index + 1}/{len(questions)}</b>\n\n"
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
            get_text("en", "new_challenge"),
            show_alert=True
        )
        return

    language = session["language"]

    questions = QUESTIONS.get(
        language,
        QUESTIONS["en"]
    )

    question = questions[question_index]

    if answer_index == question["correct"]:
        session["correct"] += 1
        session["iq"] += question["points"]

        feedback = get_text(
            language,
            "correct"
        )

    else:
        feedback = get_text(
            language,
            "wrong"
        )

    await callback.answer(feedback)

    session["question"] += 1

    if session["question"] >= len(questions):
        await finish_quiz(
            callback.message,
            user_id
        )
        return

    await send_question(
        callback.message,
        user_id
    )


async def finish_quiz(message: Message, user_id: int):
    session = quiz_sessions[user_id]

    iq = session["iq"]
    correct = session["correct"]
    language = session["language"]

    accuracy = round(
        (correct / 5) * 100
    )

    rank = get_rank(iq)

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
        reply_markup=channel_keyboard(
            CHANNEL_URL
        )
    )

    quiz_sessions.pop(
        user_id,
        None
    )


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    user = await get_user(
        callback.from_user.id
    )

    if not user:
        await callback.answer(
            get_text("en", "profile_error"),
            show_alert=True
        )
        return

    (
        user_id,
        username,
        language,
        iq,
        questions,
        correct
    ) = user

    language = language or "en"

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
