from telegram import Update
from telegram.ext import ContextTypes
from comandos.utils import verificar_usuario, registrar_usuario

async def me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    id_tg = str(user.id)
    username = user.username or user.full_name or "Sin username"

    registrar_usuario(id_tg, username)
    valido, info = verificar_usuario(id_tg)
    if not valido:
        await update.message.reply_text("No tienes cuenta registrada aún.")
        return

    ilimitado = info.get("ilimitado", False)
    creditos = info.get("CREDITOS", 0)
    await update.message.reply_text(
        f"👤 Usuario: @{username}\n💳 Créditos: {'∞' if ilimitado else creditos}",
        parse_mode="HTML"
    )