from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

class MonChatbotIoT(ActivityHandler):
   async def on_message_activity(self, turn_context: TurnContext):
    message = turn_context.activity.text.lower()
    
    # Gestion de commandes IoT simples
    if "température" in message:
        reponse = "🌡️ La température actuelle est de 22°C"
    elif "lumière" in message and "allumer" in message:
        reponse = "💡 Lumière allumée"
    elif "lumière" in message and "éteindre" in message:
        reponse = "🔌 Lumière éteinte"
    elif "aide" in message:
        reponse = "Je peux vous aider avec : température, allumer/éteindre lumière"
    else:
        reponse = f"Commande non reconnue. Tapez 'aide' pour voir les options."
    
    await turn_context.send_activity(reponse)
    
    async def on_members_added_activity(
        self, members_added: list[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Bonjour ! Je suis votre assistant IoT.")