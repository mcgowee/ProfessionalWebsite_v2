from openai import OpenAI
import psycopg2
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(
    filename="test_chatbot.log",  # Log file name
    level=logging.DEBUG,         # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
)

# Test log messages
#logging.debug("This is a DEBUG message.")
#logging.info("This is an INFO message.")
#logging.warning("This is a WARNING message.")
#logging.error("This is an ERROR message.")
#logging.critical("This is a CRITICAL message.")

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

# Database connection details
DB_PARAMS = {
    "dbname": os.environ.get("DB_NAME", "chatbot_db"),
    "user": os.environ.get("DB_USER", "chatbot_user"),
    "password": os.environ.get("DB_PASSWORD", "securepassword"),
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
}

def get_conversation_history(session_id, limit=10):
    """
    Retrieve the most recent conversation history for a session.

    Args:
        session_id (str): The session ID to filter messages.
        limit (int): The number of recent messages to retrieve.

    Returns:
        list: A list of messages in the format required by OpenAI GPT.
    """
    try:
        with psycopg2.connect(connect_timeout=3, **DB_PARAMS) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT user_message, bot_reply FROM conversation "
                    "WHERE session_id = %s ORDER BY timestamp DESC LIMIT %s",
                    (session_id, limit)
                )
                rows = cursor.fetchall()

                # Debugging: Log the retrieved history
                logging.info(f"Retrieved Conversation History for session {session_id}:")
                for row in rows:
                    logging.info(f"User: {row[0]}, Bot: {row[1]}")

                # Format messages for GPT
                messages = []
                for row in reversed(rows):  # Reverse to maintain chronological order
                    messages.append({"role": "user", "content": row[0]})
                    messages.append({"role": "assistant", "content": row[1]})

                return messages
    except Exception as e:
        logging.info(f"Error retrieving conversation history: {e}")
        return []


def save_message_to_db(session_id, user_message, bot_reply):
    """
    Save the user message and bot reply to the database.
    """
    try:
        logging.info(f"Attempting to save message to database...")
        logging.info(f"Session ID: {session_id}")
        logging.info(f"User Message: {user_message}")
        logging.info(f"Bot Reply: {bot_reply}")

        with psycopg2.connect(connect_timeout=3, **DB_PARAMS) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO conversation (session_id, user_message, bot_reply, timestamp) VALUES (%s, %s, %s, %s)",
                    (session_id, user_message, bot_reply, datetime.now())
                )
                conn.commit()  # Explicitly commit the transaction
                logging.info("Message saved successfully.")
    except Exception as e:
        logging.info(f"Error saving message to database: {e}")

def process_message(user_message, session_id):
    """
    Process the user message, save the conversation to the database, and return a response.

    Args:
        user_message (str): The message from the user.
        session_id (str): The session ID for tracking conversations.

    Returns:
        str: The chatbot's response from OpenAI GPT.
    """
    if not client.api_key:
        return "Server is missing OPENAI_API_KEY."

    try:
        # Retrieve recent conversation history for the session
        conversation_history = get_conversation_history(session_id, limit=20)

        # Add a system prompt to establish context
        system_prompt = {
            "role": "system",
            "content": (
                "You are a helpful assistant. Remember the user's name and key details "
                "shared during the conversation."
            )
        }

        # Add the current user message to the context
        conversation_history.append({"role": "user", "content": user_message})

        # **Log the conversation history for debugging**
        logging.info("Conversation History Sent to GPT:")
        for msg in [system_prompt, *conversation_history]:
            logging.info(f"{msg['role']}: {msg['content']}")

        # Call OpenAI GPT model with the conversation history
        completion = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[system_prompt, *conversation_history]
        )

        # Extract the reply from the completion object
        message_content = completion.choices[0].message.content

        # Save the conversation to the database
        save_message_to_db(session_id, user_message, message_content)

        return message_content

    except Exception as e:
        logging.debug(f"Error communicating with OpenAI API: {e}")
        return "I'm sorry, I couldn't process your request at the moment. Please try again later."