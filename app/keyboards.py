from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


LANGUAGES = {
    "en": "🇬🇧 English",
    "es": "🇪🇸 Español",
    "ar": "🇸🇦 العربية",
    "fr": "🇫🇷 Français",
    "de": "🇩🇪 Deutsch",
    "it": "🇮🇹 Italiano",
    "pt": "🇵🇹 Português",
}


def language_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                text="🇬🇧 English",
                callback_data="lang:en"
            ),
            InlineKeyboardButton(
                text="🇪🇸 Español",
                callback_data="lang:es"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🇸🇦 العربية",
                callback_data="lang:ar"
            ),
            InlineKeyboardButton(
                text="🇫🇷 Français",
                callback_data="lang:fr"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🇩🇪 Deutsch",
                callback_data="lang:de"
            ),
            InlineKeyboardButton(
                text="🇮🇹 Italiano",
                callback_data="lang:it"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🇵🇹 Português",
                callback_data="lang:pt"
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def start_quiz_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔥 Start the Challenge",
                    callback_data="start_quiz"
                )
            ]
        ]
    )


def question_keyboard(question_index: int, options: list[str]):
    buttons = []

    for index, option in enumerate(options):
        buttons.append([
            InlineKeyboardButton(
                text=option,
                callback_data=f"answer:{question_index}:{index}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def channel_keyboard(channel_url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⚽ Join Football Lovers",
                    url=channel_url
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 My Profile",
                    callback_data="profile"
                )
            ]
        ]
    )
