import sqlite3
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure Gemini model
llm = ChatGoogleGenerativeAI(api_key = "your api key",model="gemini-2.0-flash")

# Database setup
def init_db():
    conn = sqlite3.connect("mistakes.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            mistake TEXT,
            correction TEXT,
            context TEXT
        )
    """
    )
    conn.commit()
    return conn

db = init_db()

# In-memory session storage
session_data = {}

def start(user, learning_language, known_language, level):
    session_data[user] = {
        "learning_language": learning_language,
        "known_language": known_language,
        "level": level,
        "conversation": []
    }
    print(f"Welcome {user}! Let's start learning {learning_language} are you ready...")
    



def chat(user, message):
    if user not in session_data:
        return "Session not started. Use start() first."
    

    system_message = (
    f"You are a friendly and engaging language tutor. The user is learning {session_data[user]['learning_language']} "
    f"and their known language is {session_data[user]['known_language']}. "
    f"Their proficiency level is {session_data[user]['level']}. "
    "Your role is to help them learn through natural conversation, short interactive lessons, and fun quizzes. "
    "Be conversational and interactive, keeping explanations short and engaging. "
    "Ask only one or two follow-up questions per topic. "
    "If the user makes a mistake, naturally correct them using the word 'Corrected' followed by the correct answer and a brief explanation. "
    "Do not introduce sections like 'Explanation of Answers:'. Instead, keep responses flowing naturally. "
    "Adapt your responses based on the user's level:\n"
    "- Beginner: Use simple words and short sentences.\n"
    "- Intermediate: Provide moderate detail with suggestions for improvement.\n"
    "- Advanced: Use fluent, natural phrasing and provide deeper insights."
)




    prompt = f"{system_message}\n\nUser: {message}\n\nAssistant:"
    response = llm.invoke(prompt)
    bot_reply = response.content if hasattr(response, 'content') else response

    # Store conversation
    session_data[user]["conversation"].append({"user": message, "bot": bot_reply})

    # Identify mistakes (extract them properly)
    mistakes = []
    if "Corrected:" in bot_reply:
        parts = bot_reply.split("Corrected:")
        if len(parts) > 1:
            correction = parts[1].split("\n")[0].strip()
            mistakes.append({"mistake": message, "correction": correction, "context": message})
            db.execute(
                "INSERT INTO mistakes (user, mistake, correction, context) VALUES (?, ?, ?, ?)",
                (user, message, correction, message),
            )
            db.commit()
    
    return {"bot": bot_reply, "mistakes": mistakes}

def review(user):
    cursor = db.execute("SELECT mistake, correction FROM mistakes WHERE user = ?", (user,))
    mistakes = cursor.fetchall()
    
    conversation_history = session_data[user].get("conversation", [])
    mistakes_summary = "\n".join([f"Mistake: {m[0]} | Correction: {m[1]}" for m in mistakes])
    
    review_prompt = f"Based on the following conversation and mistakes, generate a personalized review for the user. Provide feedback on their progress, areas they need to improve, and encouragement for further learning.\n\nConversation:\n{conversation_history}\n\nMistakes:\n{mistakes_summary}"
    response = llm.invoke(review_prompt)
    return response.content if hasattr(response, 'content') else response

# Auto-start the chatbot
if __name__ == "__main__":
    user = input("Enter your name: ")
    learning_language = input("What language do you want to learn? ")
    known_language = input("What language do you know? ")
    level = input("What is your level in the learning language? (Beginner/Intermediate/Advanced) ")
    
    start(user, learning_language, known_language, level)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye! Here's your mistake review:")
            print(review(user))
            break
        response = chat(user, user_input)
        print("Bot:", response["bot"])
