import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("8767843965:AAGrX0PMcBFv7dyUEDf8WCFY2rmyMLaHKc4")

LINK_25 = "https://pay.kirvano.com/962361f0-a5d2-41e8-82a6-422f0b315cb8"
LINK_60 = "https://pay.kirvano.com/7af1874d-b810-4366-964c-8d14c1fe581c"

GRUPO_25 = "t.me/melvalierr"
GRUPO_60 = "t.me/melvaliervip"

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.first_name

    await update.message.reply_text(
        f"oi {user}... 😏\n\n"
        "tava te esperando aqui..."
    )

    # FOTO PRÉVIA
    with open("previa.mp4", "rb") as video:
        await update.message.reply_video(
            video=video,
            caption="😈 isso aqui é só uma prévia...\n\n"
                    "o resto eu não mostro aqui..."
        )


    # BOTÕES
    keyboard = [
        [InlineKeyboardButton("💋 Ver agora (pacote simples) (R$25)", callback_data="plano_25")],
        [InlineKeyboardButton("🔥 Quero tudo (pacote completo) (R$60)", callback_data="plano_60")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👇 escolhe como quer me ver:",
        reply_markup=reply_markup,
    )


# =========================
# ESCOLHA DE PLANO
# =========================
async def escolher_plano(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    plano = query.data
    context.user_data["plano"] = plano

    if plano == "plano_25":
        await query.message.reply_text(
            "💋 boa escolha...\n\n"
            "👇 paga aqui:\n"
            f"{LINK_25}\n\n"
            "me manda o comprovante pra liberar 😏"
        )

    elif plano == "plano_60":
        await query.message.reply_text(
            "🔥 sabia que você queria tudo...\n\n"
            "👇 paga aqui:\n"
            f"{LINK_60}\n\n"
            "me manda o comprovante 💋"
        )


# =========================
# RECEBER COMPROVANTE
# =========================
async def receber_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):

    plano = context.user_data.get("plano")

    # SE ENVIOU FOTO
    if update.message.photo:

        if plano == "plano_25":
            await update.message.reply_text(
                "😏 já vi aqui...\n\n"
                "👇 solicita entrada:\n"
                f"{GRUPO_25}\n\n"
                "te aceito lá 💋"
            )

        elif plano == "plano_60":
            await update.message.reply_text(
                "🔥 perfeito...\n\n"
                "👇 entra no VIP:\n"
                f"{GRUPO_60}\n\n"
                "já já te libero 😈"
            )

        else:
            await update.message.reply_text(
                "😅 você ainda não escolheu um plano...\n"
                "digita /start e escolhe 😉"
            )

    else:
        await update.message.reply_text(
            "me envia o comprovante em FOTO pra liberar 😉"
        )


# =========================
# ERROS (IMPORTANTE)
# =========================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Erro: {context.error}")


# =========================
# MAIN
# =========================
def main():

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(escolher_plano))
    app.add_handler(MessageHandler(filters.ALL, receber_comprovante))
    app.add_error_handler(error_handler)

    print("Bot rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()
