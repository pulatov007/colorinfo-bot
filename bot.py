from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random
import colorsys

TOKEN = "8643125015:AAFcVRtGjTKUtGoU8hu9ag_HcqiAuBiLGSI"


def hex_to_rgb(hex_color):
    hex_color = hex_color.strip().lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b


def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def is_valid_hex(text):
    text = text.strip().lstrip("#")
    if len(text) == 6:
        try:
            int(text, 16)
            return True
        except:
            return False
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am Color Info Bot 🎨\n\n"
        "Send me a hex color like #FF5733 and I will tell you info about it.\n\n"
        "Commands:\n"
        "/random - get a random color\n"
        "/palette #HEX - get 5 similar colors\n"
        "/complementary #HEX - get the opposite color\n"
        "/help - show this message"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "How to use this bot:\n\n"
        "Just send a hex color code like:\n"
        "#FF5733\n"
        "#3A86FF\n"
        "#00FF00\n\n"
        "Commands:\n"
        "/random - get a random color\n"
        "/palette #HEX - get 5 similar colors\n"
        "/complementary #HEX - get the opposite color"
    )


async def random_color(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    hex_color = rgb_to_hex(r, g, b)

    await update.message.reply_text(
        f"🎲 Random Color!\n\n"
        f"HEX: {hex_color}\n"
        f"RGB: {r}, {g}, {b}"
    )


async def palette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a color. Example: /palette #FF5733")
        return

    text = context.args[0]
    if not is_valid_hex(text):
        await update.message.reply_text("That does not look like a hex color. Example: /palette #FF5733")
        return

    r, g, b = hex_to_rgb(text)

    # shift hue slightly 5 times to get similar colors
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    colors = []
    for i in range(5):
        new_h = (h + 0.08 * i) % 1.0
        nr, ng, nb = colorsys.hsv_to_rgb(new_h, s, v)
        colors.append(rgb_to_hex(round(nr * 255), round(ng * 255), round(nb * 255)))

    result = "🎨 Palette (5 similar colors):\n\n"
    for c in colors:
        result += f"{c}\n"

    await update.message.reply_text(result)


async def complementary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a color. Example: /complementary #FF5733")
        return

    text = context.args[0]
    if not is_valid_hex(text):
        await update.message.reply_text("That does not look like a hex color. Example: /complementary #FF5733")
        return

    r, g, b = hex_to_rgb(text)

    # opposite color = shift hue by 180 degrees (0.5)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    new_h = (h + 0.5) % 1.0
    cr, cg, cb = colorsys.hsv_to_rgb(new_h, s, v)
    comp_hex = rgb_to_hex(round(cr * 255), round(cg * 255), round(cb * 255))

    await update.message.reply_text(
        f"🔄 Complementary Color\n\n"
        f"Original:      {rgb_to_hex(r, g, b)}\n"
        f"Complementary: {comp_hex}"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not is_valid_hex(text):
        await update.message.reply_text("That does not look like a hex color. Try something like #FF5733")
        return

    r, g, b = hex_to_rgb(text)
    hex_color = rgb_to_hex(r, g, b)

    await update.message.reply_text(
        f"🎨 Color Info\n\n"
        f"HEX: {hex_color}\n"
        f"RGB: {r}, {g}, {b}"
    )


async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Welcome message"),
        BotCommand("random", "Get a random color"),
        BotCommand("palette", "Get 5 similar colors"),
        BotCommand("complementary", "Get the opposite color"),
        BotCommand("help", "Show all commands"),
    ])


app = ApplicationBuilder().token(TOKEN).connect_timeout(30).read_timeout(30).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("random", random_color))
app.add_handler(CommandHandler("palette", palette))
app.add_handler(CommandHandler("complementary", complementary))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.post_init = set_commands
app.run_polling()
