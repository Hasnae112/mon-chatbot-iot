from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from bot import MonChatbotIoT
import os

# Configuration
APP_ID = os.environ.get("MICROSOFT_APP_ID", "")
APP_PASSWORD = os.environ.get("MICROSOFT_APP_PASSWORD", "")

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
    # Azure uses PORT 8000
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)