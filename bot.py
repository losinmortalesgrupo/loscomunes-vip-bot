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
            "para personas fit con cuerpo atlético (NO FLACOS O GORDOS, SÓLO MUSCULOSOS).\n\n"

            "SERÁ REVISADO POR UNA PERSONA REAL.\n\n"
"NO ENVIES INFORMACIÓN FALSA, NO ENGAÑARAS A NADIE.\n"
"Las solicitudes falsas serán rechazadas y recibirás ban.\n\n"

            "PARA COMENZAR:\n"
            "DECÍ TU EDAD 👀"
        ),

        "ask_video": (
            "Perfecto.\n\n"

            "Ahora enviá un VIDEO DESNUDO permanente grabado "
            "en modo manos libres.\n\n"

            "Debés posar mostrando músculos 💪🦵:\n"
            "• de frente\n"
            "• y de espalda\n\n"

            "El video debe verse claramente."
        ),

        "invalid_video":
            "⚠️ Tenés que enviar un VIDEO válido.",

        "photo_not_allowed":
            "⚠️ No se aceptan fotos.\n\n"
            "Debés enviar un VIDEO.",

        "warning": (
            "⚠️ ÚLTIMO AVISO.\n\n"

            "Tu solicitud continúa sin completar la verificación.\n\n"

            "Esta NO es una verificación falsa o simulada.\n\n"

            "Si no completás la verificación obligatoria "
            "de este bot, el acceso al grupo será "
            "DENEGADO PERMANENTEMENTE.\n\n"

            "No existe otra forma de ingresar.\n\n"

            "Tu solicitud será eliminada."
        ),

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

            "This bot verifies access to an exclusive hot group "
            "for fit people with athletic bodies (NOT SKINNY OR FAT, ONLY MUSCULAR).\n\n"

            " THE INFORMATION REVIEWED BY A REAL PERSON.\n\n"
            " DO NOT SEND FALSE INFORMATION, YOU WIIL NOT DECEIVE ANYONED.\n"
            "Fake applications will be rejected and banned.\n\n"
            
            "TO BEGIN:\n"
            "TELL YOUR AGE 👀"
        ),

        "ask_video": (
            "Perfect.\n\n"

            "Now send a permanent NAKED VIDEO recorded "
            "hands-free.\n\n"

            "You must pose showing muscles 💪🦵:\n"
            "• front\n"
            "• back\n\n"

            "The video must be clearly visible."
        ),

        "invalid_video":
            "⚠️ You must send a valid VIDEO.",

        "photo_not_allowed":
            "⚠️ Photos are not accepted.\n\n"
            "You must send a VIDEO.",

        "warning": (
            "⚠️ FINAL WARNING.\n\n"

            "Your request is still incomplete.\n\n"

            "This is NOT a fake or simulated verification.\n\n"

            "If you do not complete the mandatory verification "
            "required by this bot, access to the group "
            "will be PERMANENTLY DENIED.\n\n"

            "There is no other way to join.\n\n"

            "Your request will be deleted."
        ),

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

            "Este bot verifica a entrada em um grupo hot exclusivo "
            "para pessoas fitness com corpo atlético (NEM MAGRO NEM GORDO, SÓ MUSCULOSO).\n\n"

            "Será analisado por uma pessoa real.\n\n"
"Não envie informações falsas.\n"
"Solicitações falsas serão rejeitadas e banidas.\n\n"

            "PARA COMEÇAR:\n"
            "DIGA SUA IDADE 👀"
        ),

        "ask_video": (
            "Perfeito.\n\n"

            "Agora envie um VÍDEO NU permanente gravado "
            "em modo mãos livres.\n\n"

            "Você deve posar mostrando os músculos 💪🦵:\n"
            "• frente\n"
            "• costas\n\n"

            "O vídeo deve estar claramente visível."
        ),

        "invalid_video":
            "⚠️ Você precisa enviar um VÍDEO válido.",

        "photo_not_allowed":
            "⚠️ Fotos não são aceitas.\n\n"
            "Você deve enviar um VÍDEO.",

        "warning": (
            "⚠️ AVISO FINAL.\n\n"

            "Sua solicitação ainda está incompleta.\n\n"

            "Esta NÃO é uma verificação falsa ou simulada.\n\n"

            "Se você não concluir a verificação obrigatória "
            "deste bot, o acesso ao grupo será "
            "NEGADO PERMANENTEMENTE.\n\n"

            "Não existe outra forma de entrar.\n\n"

            "Sua solicitação será removida."
        ),

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

    # Aviso automático después de 10 minutos
    context.job_queue.run_once(
        send_warning,
        600,
        data=user.id
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

async def send_warning(context: ContextTypes.DEFAULT_TYPE):

    user_id = context.job.data

    if user_id not in pending_users:
        return

    step = pending_users[user_id].get("step")

    # Si ya terminó verificación no enviar aviso
    if step == "done":
        return

    lang = pending_users[user_id].get("lang", "es")

    try:

        await context.bot.send_message(
            chat_id=user_id,
            text=TEXTS[lang]["warning"]
        )

    except:
        pass

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
