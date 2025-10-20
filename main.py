import asyncio
import os
import json
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from comandos.utils import init_users
from comandos.me import me_command
from comandos.movistar import movistar_command
from comandos.admin_requests import reply_request, forward_file, init_db
from aiohttp import web

TOKEN = None
try:
    with open("config.json", "r", encoding="utf-8") as f:
        CFG = json.load(f)
        TOKEN = CFG.get("BOT_TOKEN")
except Exception as e:
    print("Error loading config.json:", e)

if not TOKEN:
    raise SystemExit("BOT_TOKEN no encontrado en config.json")

async def run_bot():
    init_users()
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("me", me_command))
    app.add_handler(CommandHandler("start", me_command))
    app.add_handler(CommandHandler("movistar", movistar_command))
    app.add_handler(CommandHandler("reply", reply_request))
    app.add_handler(CommandHandler("adminsend", forward_file))

    async def echo(update, context):
        await update.message.reply_text("Comando no reconocido. Usa /me o /movistar <número>.")

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("Bot corriendo en modo polling...")
    await app.run_polling()

async def web_alive(request):
    return web.Response(text="Bot activo en Render ✅")

async def main():
    # iniciar polling en segundo plano
    asyncio.create_task(run_bot())

    # iniciar servidor web
    app = web.Application()
    app.add_routes([web.get("/", web_alive)])
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web escuchando en puerto {port}")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
