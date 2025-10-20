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

# ---------- BOT ----------
async def start_bot(app):
    print("✅ Iniciando bot con polling (Render web mode)...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

# ---------- Servidor web ----------
async def web_alive(request):
    return web.Response(text="🤖 Bot activo en Render")

async def main():
    init_users()
    init_db()

    # Configurar bot
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("me", me_command))
    app.add_handler(CommandHandler("start", me_command))
    app.add_handler(CommandHandler("bloqueo", bloqueo_command))
    app.add_handler(CommandHandler("reply", reply_request))
    app.add_handler(CommandHandler("adminsend", forward_file))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: u.message.reply_text("Comando no reconocido.")))

    # Iniciar el bot sin cerrar el loop
    asyncio.create_task(start_bot(app))

    # Iniciar servidor HTTP para Render
    app_web = web.Application()
    app_web.add_routes([web.get("/", web_alive)])
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Servidor web escuchando en puerto {port}")

    # Mantener el proceso activo
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
