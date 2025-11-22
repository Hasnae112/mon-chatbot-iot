from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import datetime

class MonChatbotIoT(ActivityHandler):
    def __init__(self):
        # Simuler l'état des appareils IoT
        self.devices = {
            "lumière": False,
            "ventilateur": False,
            "température": 22
        }
    
    async def on_message_activity(self, turn_context: TurnContext):
        message = turn_context.activity.text.lower()
        
        # Commande: Température
        if "température" in message or "temp" in message:
            temp = self.devices["température"]
            reponse = f"🌡️ La température actuelle est de {temp}°C"
        
        # Commande: Lumière
        elif "lumière" in message or "lumiere" in message:
            if "allumer" in message or "on" in message:
                self.devices["lumière"] = True
                reponse = "💡 Lumière allumée avec succès !"
            elif "éteindre" in message or "off" in message:
                self.devices["lumière"] = False
                reponse = "🔌 Lumière éteinte avec succès !"
            else:
                status = "allumée" if self.devices["lumière"] else "éteinte"
                reponse = f"💡 La lumière est actuellement {status}"
        
        # Commande: Ventilateur
        elif "ventilateur" in message or "fan" in message:
            if "allumer" in message or "on" in message:
                self.devices["ventilateur"] = True
                reponse = "🌀 Ventilateur allumé avec succès !"
            elif "éteindre" in message or "off" in message:
                self.devices["ventilateur"] = False
                reponse = "⭕ Ventilateur éteint avec succès !"
            else:
                status = "allumé" if self.devices["ventilateur"] else "éteint"
                reponse = f"🌀 Le ventilateur est actuellement {status}"
        
        # Commande: État de tous les appareils
        elif "état" in message or "etat" in message or "status" in message:
            lumiere_status = "✅ Allumée" if self.devices["lumière"] else "❌ Éteinte"
            ventilateur_status = "✅ Allumé" if self.devices["ventilateur"] else "❌ Éteint"
            reponse = f"""📊 État des appareils IoT:
            
💡 Lumière: {lumiere_status}
🌀 Ventilateur: {ventilateur_status}
🌡️ Température: {self.devices["température"]}°C

Dernière mise à jour: {datetime.datetime.now().strftime('%H:%M:%S')}"""
        
        # Commande: Aide
        elif "aide" in message or "help" in message:
            reponse = """🤖 Commandes disponibles:

📍 **Température:**
   • "température" - Voir la température actuelle

💡 **Lumière:**
   • "allumer lumière" - Allumer la lumière
   • "éteindre lumière" - Éteindre la lumière

🌀 **Ventilateur:**
   • "allumer ventilateur" - Allumer le ventilateur
   • "éteindre ventilateur" - Éteindre le ventilateur

📊 **Général:**
   • "état" - Voir l'état de tous les appareils
   • "aide" - Afficher ce message"""
        
        # Commande non reconnue
        else:
            reponse = f"❓ Commande '{message}' non reconnue. Tapez 'aide' pour voir les options disponibles."
        
        await turn_context.send_activity(reponse)
    
    async def on_members_added_activity(
        self, members_added: list[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "👋 Bonjour ! Je suis votre assistant IoT.\n\n"
                    "Je peux vous aider à contrôler vos appareils connectés.\n"
                    "Tapez 'aide' pour voir toutes les commandes disponibles !"
                )