import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ChatJoinRequestHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8650638236:AAFW9UlDhm-uoPXlGdI1EDax9p_933cW2aQ"

pending_users = {}

GROUP_ID = -1003707089986

ADMIN_ID = 8011642705

TEXTS = {

    "es": {

        "welcome": (
            "🔒 Bienvenido al sistema de verificación.\n\n"

            "Este bot verifica el ingreso a un grupo hot exclusivo "
            "para personas fit con cuerpo atlético.\n\n"

            "LA INFORMACION ENVIADA SERA REVISADA MANUALMENTE "
            "POR UNA PERSONA REAL.\n\n"

            "NO ENVIES INFORMACIÓN FALSA O CONTENIDO INCORRECTO "
            "NI CONTENIDO INVALIDO.\n\n"

            "NO VAS A ENGAÑAR A NADIE.\n"
            "LAS SOLICITUDES ENGAÑOSAS SERAN RECHZADAS Y BAN FEDERATIVO DE TODOS LOS GRUPOS.\n\n"

            "PARA COMENZAR:\n"
            "DECÍ TU EDAD 👀"
        ),

        "ask_video": (
            "Perfecto.\n\n"

            "Ahora enviá un VIDEO DESNUDO permanente grabado "
            "en modo manos libres.\n\n"

            "Debés posar mostrando músculos💪🦵:\n"
            "• de frente\n"
            "• y de espalda\n\n"

            "El video debe verse claramente."
        ),

        "invalid_video":
            "⚠️ Tenés que enviar un VIDEO válido.",

        "photo_not_allowed":
            "⚠️ No se aceptan fotos.\n\n"
            "Debés enviar un VIDEO.",

        "sent":
            "✅ Solicitud enviada para revisión.",

        "approved":
            "✅ Tu solicitud fue aprobada.",

        "rejected":
            "❌ Tu solicitud fue rechazada.",
    },

    "en": {

        "welcome": (
            "🔒 Welcome to the verification system.\n\n"

            "This bot verifies access to an exclusive group "
            "for fit people with athletic bodies.\n\n"

           "THE INFORMATION SUBMITTED WILL BE MANUALLY REVIEWED"

"BY A REAL PERSON."\n\n"

"DO NOT SEND FALSE INFORMATION OR INCORRECT CONTENT"

"OR INVALID CONTENT."\n\n"

"YOU WILL NOT DECEIVE ANYONE."\n"

"DECEPTIVE APPLICATIONS WILL BE REJECTED AND WILL RESULT IN A FEDERAL BAN FROM ALL GROUPS."\n\n"

            "TO BEGIN:\n"
            "TELL YOUR AGE 👀"
        ),

        "ask_video": (
            "Perfect.\n\n"

            "Now send a permanent VIDEO recorded "
            "hands-free.\n\n"

            "You must pose showing muscles💪🦵:\n"
            "• front\n"
            "• back\n\n"

            "The video must be clearly visible."
        ),

        "invalid_video":
            "⚠️ You must send a valid VIDEO.",

        "photo_not_allowed":
            "⚠️ Photos are not accepted.\n\n"
            "You must send a VIDEO.",

        "sent":
            "✅ Request sent for review.",

        "approved":
            "✅ Your request was approved.",

        "rejected":
            "❌ Your request was rejected.",
    },

    "pt": {

        "welcome": (
            "🔒 Bem-vindo ao sistema de verificação.\n\n"

            "Este bot verifica a entrada em um grupo exclusivo "
            "para pessoas fitness com corpo atlético.\n\n"

           "AS INFORMAÇÕES ENVIADAS SERÃO ANALISADAS MANUALMENTE"

"POR UMA PESSOA REAL."\n\n"

"NÃO ENVIE INFORMAÇÕES FALSAS OU CONTEÚDO INCORRETO"

"OU CONTEÚDO INVÁLIDO."\n\n"

"VOCÊ NÃO ENGANARÁ NINGUÉM."\n"

"CANDIDATURAS ENGANOSAS SERÃO REJEITADAS E RESULTARÃO EM BANIMENTO FEDERAL DE TODOS OS GRUPOS."\n\n"

            "PARA COMEÇAR:\n"
            "DIGA SUA IDADE 👀"
        ),

        "ask_video": (
            "Perfeito.\n\n"

            "Agora envie um VÍDEO permanente gravado "
            "em modo mãos livres.\n\n"

            "Você deve posar mostrando os músculos💪🦵:\n"
            "• frente\n"
            "• costas\n\n"

            "O vídeo deve estar claramente visível."
        ),

        "invalid_video":
            "⚠️ Você precisa enviar um VÍDEO válido.",

        "photo_not_allowed":
            "⚠️ Fotos não são aceitas.\n\n"
            "Você deve enviar um VÍDEO.",

        "sent":
            "✅ Solicitação enviada para revisão.",

        "approved":
            "✅ Sua solicitação foi aprovada.",

        "rejected":
            "❌ Sua solicitação foi rejeitada.",
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("Español", callback_data="lang_es"),
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("Português", callback_data="lang_pt"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Seleccioná tu idioma / Select your language / Selecione seu idioma",
        reply_markup=reply_markup
    )


async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    lang = query.data.split("_")[1]

    user = query.from_user

    if user.id not in pending_users:
        pending_users[user.id] = {}

    pending_users[user.id]["step"] = "age"
    pending_users[user.id]["lang"] = lang
    pending_users[user.id]["username"] = user.username
    pending_users[user.id]["name"] = user.full_name

    await query.edit_message_text(
        TEXTS[lang]["welcome"]
    )


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.chat_join_request.from_user

    group_id = update.chat_join_request.chat.id

    if group_id != GROUP_ID:
        return

    pending_users[user.id] = {
        "group_id": group_id
    }

    keyboard = [
        [
            InlineKeyboardButton("Español", callback_data="lang_es"),
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("Português", callback_data="lang_pt"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:

        await context.bot.send_message(
            chat_id=user.id,
            text=(
                "🔒 Verification Bot\n\n"

                "Seleccioná tu idioma.\n"
                "Select your language.\n"
                "Selecione seu idioma."
            ),
            reply_markup=reply_markup
        )

    except Exception as e:
        print(f"No se pudo enviar mensaje: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.type != "private":
        return

    user_id = update.effective_user.id

    if user_id not in pending_users:
        return

    step = pending_users[user_id].get("step")

    lang = pending_users[user_id].get("lang", "es")

    if step == "age":

        if not update.message.text:

            await update.message.reply_text(
                "Send only your age in numbers."
            )
            return

        if not update.message.text.isdigit():

            await update.message.reply_text(
                "Send only your age in numbers."
            )
            return

        pending_users[user_id]["age"] = update.message.text

        pending_users[user_id]["step"] = "video"

        await update.message.reply_text(
            TEXTS[lang]["ask_video"]
        )

    elif step == "video":

        if update.message.photo:

            await update.message.reply_text(
                TEXTS[lang]["photo_not_allowed"]
            )

            return

        if update.message.video:

            age = pending_users[user_id]["age"]

            username = pending_users[user_id].get("username")

            name = pending_users[user_id].get("name")

            username_text = (
                f"@{username}"
                if username else "Sin @username"
            )

            await context.bot.send_video(
                chat_id=ADMIN_ID,
                video=update.message.video.file_id,
                caption=(
                    f"📥 Nueva solicitud\n\n"

                    f"👤 Nombre: {name}\n"
                    f"🔗 Usuario: {username_text}\n"
                    f"🆔 ID: {user_id}\n"
                    f"🎂 Edad: {age}\n\n"

                    f"/aprobar {user_id}\n"
                    f"/rechazar {user_id}"
                )
            )

            await update.message.reply_text(
                TEXTS[lang]["sent"]
            )

            pending_users[user_id]["step"] = "done"

        else:

            await update.message.reply_text(
                TEXTS[lang]["invalid_video"]
            )


async def aprobar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    user_id = int(context.args[0])

    group_id = pending_users[user_id]["group_id"]

    await context.bot.approve_chat_join_request(
        chat_id=group_id,
        user_id=user_id
    )

    await context.bot.send_message(
        user_id,
        "✅ Approved."
    )

    await update.message.reply_text(
        "Usuario aprobado."
    )


async def rechazar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    user_id = int(context.args[0])

    group_id = pending_users[user_id]["group_id"]

    await context.bot.decline_chat_join_request(
        chat_id=group_id,
        user_id=user_id
    )

    await context.bot.send_message(
        user_id,
        "❌ Rejected."
    )

    await update.message.reply_text(
        "Usuario rechazado."
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(language_selected))

app.add_handler(ChatJoinRequestHandler(join_request))

app.add_handler(
    MessageHandler(
        ~filters.COMMAND,
        handle_message
    )
)

app.add_handler(CommandHandler("aprobar", aprobar))

app.add_handler(CommandHandler("rechazar", rechazar))

print("Bot iniciado...")

app.run_polling()
