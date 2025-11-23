from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from bot import MonChatbotIoT
import os

# Configuration: Use Azure's standard environment variable names (case-sensitive on Linux)
APP_ID = os.environ.get("MicrosoftAppId", "")
APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

# Create adapter
settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

# Create bot instance
bot = MonChatbotIoT()

# Handle incoming /api/messages requests
async def messages(req: web.Request) -> web.Response:
    if "application/json" not in req.headers.get("Content-Type", ""):
        return web.Response(status=415, text="Unsupported Media Type")

    try:
        body = await req.json()
        activity = Activity().deserialize(body)
        auth_header = req.headers.get("Authorization", "")

        # Process the activity with your bot
        await adapter.process_activity(activity, auth_header, bot.on_turn)
        return web.Response(status=200)

    except ValueError as e:
        # Bad JSON or deserialization error
        print(f"JSON deserialization error: {e}")
        return web.Response(status=400, text="Bad Request")
    except Exception as e:
        # Log any other error (e.g., auth failure, bot crash)
        print(f"Error processing activity: {e}")
        return web.Response(status=500, text="Internal Server Error")

# Create aiohttp application
app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    # Azure sets PORT automatically; fallback to 8000 for local testing
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)