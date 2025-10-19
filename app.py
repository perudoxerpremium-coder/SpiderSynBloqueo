from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot repository. Use worker to run the bot (Procfile: worker: python main.py)"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)