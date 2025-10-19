import asyncio
import os
import json
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from comandos.utils import init_users
from comandos.me import me_command
from comandos.movistar import movistar_command
from comandos.admin_requests import reply_request, forward_file, init_db

TOKEN = None
CFG = {}
try:
    with open("config.json", "r", encoding="utf-8") as f:
        CFG = json.load(f)
        TOKEN = CFG.get("BOT_TOKEN")
except Exception as e:
    print("Error loading config.json:", e)

if not TOKEN:
    raise SystemExit("BOT_TOKEN no encontrado en config.json. Edita config.json y añade el token.")

async def main():
    init_users()
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("me", me_command))
    app.add_handler(CommandHandler("start", me_command))
    app.add_handler(CommandHandler("movistar", movistar_command))
    app.add_handler(CommandHandler("reply", reply_request))
    # forward_file expects the admin to reply to the admin notification with a file and then run /adminsend
    app.add_handler(CommandHandler("adminsend", forward_file))

    # Simple text echo for unknown messages (optional)
    async def echo(update, context):
        await update.message.reply_text("Comando no reconocido. Usa /me o /movistar <número>.")

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot arrancando con polling...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())