from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8767843965:AAGrX0PMcBFv7dyUEDf8WCFY2rmyMLaHKc4"

LINK_25 = "https://pay.kirvano.com/962361f0-a5d2-41e8-82a6-422f0b315cb8"
LINK_60 = "https://pay.kirvano.com/2cf99dcd-fa55-43d3-9f05-d14b0be067fe"

GRUPO_25 = "https://t.me/+p9W67fbwwOdjMzFh"
GRUPO_60 = "https://t.me/+cnEDZw7j0gowOWFh"

# Quando entra no bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text("oi amor... 😏")

    with open("previa.jpg", "rb") as foto:
        await update.message.reply_photo(
            photo=foto,
            caption="😈 essa é só uma prévia..."
        )

    keyboard = [
        [InlineKeyboardButton("💋 quero ver agora (R$25)", callback_data="25")],
        [InlineKeyboardButton("🔥 Quero tudo por 1 mês (R$60)", callback_data="60")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👇 escolhe como quer me ver:",
        reply_markup=reply_markup
    )

# Quando clica no botão
async def escolher_plano(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    escolha = query.data
    context.user_data["plano"] = escolha

    if escolha == "25":
        await query.message.reply_text(
            f"💋 perfeito...\n\n"
            f"faz o pagamento aqui:\n{LINK_25}\n\n"
            f"depois me envia o comprovante 😏"
        )

    elif escolha == "60":
        await query.message.reply_text(
            f"🔥 sabia que você ia querer mais...\n\n"
            f"paga aqui:\n{LINK_60}\n\n"
            f"e me manda o comprovante 💋"
        )

# Quando envia comprovante
async def receber_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if update.message.photo:
        plano = context.user_data.get("plano")

        if plano == "25":
            await update.message.reply_text(
                f"😏 certinho...\n\n"
                f"👇 pede entrada aqui:\n{GRUPO_25}\n\n"
                f"já já te aceito 💋"
            )

        elif plano == "60":
            await update.message.reply_text(
                f"🔥 agora sim...\n\n"
                f"👇 entra no VIP:\n{GRUPO_60}\n\n"
                f"te aceito lá 😈"
            )

        else:
            await update.message.reply_text(
                "me fala qual plano você comprou 😉"
            )

    else:
        await update.message.reply_text(
            "me envia o comprovante em foto 😉"
        )

# rodar bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(escolher_plano))
app.add_handler(MessageHandler(filters.ALL, receber_comprovante))

print("Bot rodando...")
app.run_polling()