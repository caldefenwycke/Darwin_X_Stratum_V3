# utils/webhook.py
import requests

def send_discord(message):
    try:
        from core.config import discord_webhook_url
    except:
        return  # Fallback for external use if import fails

    try:
        with open("core/config.json") as f:
            import json
            config = json.load(f)
            url = config["discord"]["webhook_url"]
            if not url:
                return
            payload = {"content": message}
            requests.post(url, json=payload, timeout=3)
    except Exception as e:
        print(f"[WEBHOOK] Failed to send Discord message: {e}")
