import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# OpenAI API konfigurieren
OPENAI_API_KEY = "OpenAI_Schlüssel"
openai.api_key = OPENAI_API_KEY

# Funktion zum Übersetzen von Schweizerdeutsch auf Hochdeutsch
def translate_with_chatgpt(text: str) -> str:
    prompt = f"Übersetze den Text vom Schweizerdeutsch ins Hochdeutsch: {text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist ein Übersetzer von Schweizerdeutsch auf Hochdeutsch."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Es ist ein Fehler aufgetreten: {e}"

# Funktion zur Verarbeitung eingehender Nachrichten
async def handle_message(update: Update, context: CallbackContext) -> None:
    incoming_text = update.message.text
    translated_text = translate_with_chatgpt(incoming_text)
    await update.message.reply_text(f"Übersetzung:\n{translated_text}")

# Hauptfunktion zum Starten des Bots
def main():
    TELEGRAM_TOKEN = "Token"
    
    # Erstellung der Application zum Verarbeiten von Nachrichten
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Hinzufügen des Nachrichtenhandlers (keine Befehle erforderlich)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start des Bots
    application.run_polling()

if __name__ == '__main__':
    main()
