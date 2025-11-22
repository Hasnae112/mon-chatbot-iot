from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from bot import MonChatbotIoT
import os
import socket

# Configuration (vous les obtiendrez d'Azure plus tard)
APP_ID = ""  # Laissez vide pour les tests locaux
APP_PASSWORD = ""  # Laissez vide pour les tests locaux

# Créer l'adaptateur
settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

# Créer le bot
bot = MonChatbotIoT()

# Gérer les messages
async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    
    async def call_bot(turn_context):
        await bot.on_turn(turn_context)
    
    await adapter.process_activity(activity, auth_header, call_bot)
    return web.Response(status=200)

# Créer le serveur web
app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    def _is_port_free(port: int, host: str = "localhost") -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return True
            except OSError:
                return False

    def _find_free_port(start_port: int = 3978, host: str = "localhost", max_port: int = 4000) -> int:
        for p in range(start_port, max_port + 1):
            if _is_port_free(p, host):
                return p
        raise OSError(f"No free ports in range {start_port}-{max_port}")

    preferred_port = int(os.environ.get("PORT", "3978"))
    if not _is_port_free(preferred_port, "127.0.0.1"):
        try:
            chosen = _find_free_port(preferred_port + 1, "127.0.0.1")
            print(f"Port {preferred_port} is in use — switching to available port {chosen}.")
            preferred_port = chosen
        except OSError as ex:
            print(str(ex))
            raise

    web.run_app(app, host="localhost", port=preferred_port)