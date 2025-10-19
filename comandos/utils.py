import sqlite3, os

DB_USERS = "users.db"

def init_users():
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            username TEXT,
            CREDITOS INTEGER DEFAULT 10,
            ilimitado INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def verificar_usuario(user_id: str):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("SELECT CREDITOS, ilimitado, username FROM usuarios WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return True, {"CREDITOS": row[0], "ilimitado": bool(row[1]), "username": row[2]}
    else:
        return False, {}

def descontar_creditos(user_id: str, cantidad: int):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("UPDATE usuarios SET CREDITOS = CREDITOS - ? WHERE id=?", (cantidad, user_id))
    conn.commit()
    conn.close()

def registrar_usuario(user_id: str, username: str):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO usuarios (id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()