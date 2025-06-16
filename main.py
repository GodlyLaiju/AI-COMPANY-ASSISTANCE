import os
import gradio as gr

from src.ai_assistance import CompanyAssistanceBot
import os
from dotenv import load_dotenv

load_dotenv(override=True)
GOOGLE_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def initialize_bot():
    """Initialize and index the FAQ bot"""
    print("Initializing FAQ Bot...")
    print(GOOGLE_GEMINI_API_KEY)
    bot = CompanyAssistanceBot(
        api_key=GOOGLE_GEMINI_API_KEY,
    )

    # Index documents if data directory exists
    if os.path.exists("./source_data"):
        bot.index_documents("./source_data")
    else:
        print(
            "Warning: ./data directory not found. Please create it and add your policy documents."
        )

    return bot


# Wrap in a main block
def main():
    bot = initialize_bot()

    def bot_response(messages, chat_history):
        user_message = messages
        return bot.ask(user_message)

    gr.ChatInterface(
        bot_response,
        type="messages",
        chatbot=gr.Chatbot(height=400, type="messages"),
        description="Ask question about data",
        theme="ocean",
    ).launch(share=True)


if __name__ == "__main__":
    main()
