# Language Learning Chatbot

This is an interactive language learning chatbot that helps users practice and improve their language skills through natural conversation. The chatbot corrects mistakes, tracks progress, and provides personalized feedback using the Google Gemini AI model.

## Features
- Natural language conversation for learning.
- Mistake detection and correction.
- Conversation history tracking.
- Personalized feedback based on mistakes.
- Supports multiple languages and proficiency levels.
- SQLite database for storing user mistakes.

## Prerequisites
- Python 3.x
- Required Python packages:
  - `sqlite3` (built-in)
  - `langchain_google_genai`

## Setup and Installation
1. Clone the repository or copy the script to your local machine.
2. Install dependencies using:
   ```bash
   pip install langchain-google-genai
   ```
3. Obtain an API key for Google Gemini and replace `your api key` in the script with your actual API key.
4. Run the chatbot using:
   ```bash
   python chatbot.py
   ```

## How to Use
1. Start the chatbot and provide your name, learning language, known language, and proficiency level.
2. Engage in conversation with the chatbot.
3. The chatbot corrects mistakes and stores them in a database.
4. Type `exit`, `quit`, or `bye` to end the session.
5. Upon exit, the chatbot provides a review of your mistakes and suggestions for improvement.

## Database Structure
The chatbot uses an SQLite database (`mistakes.db`) with the following table:
```sql
CREATE TABLE mistakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    mistake TEXT,
    correction TEXT,
    context TEXT
);
```

## Functions
- `init_db()`: Initializes the database.
- `start(user, learning_language, known_language, level)`: Starts a learning session.
- `chat(user, message)`: Handles conversation, detects mistakes, and stores corrections.
- `review(user)`: Provides a personalized review based on stored mistakes.

## Example Usage
```bash
Enter your name: John
What language do you want to learn? Spanish
What language do you know? English
What is your level in the learning language? (Beginner/Intermediate/Advanced) Beginner
```
Conversation example:
```bash
You: Hola, yo soy John y querer aprender español.
Bot: Corrected: "Hola, yo soy John y quiero aprender español." ("Querer" should be conjugated as "quiero" in this context.)
```

## License
This project is open-source and available for modification and enhancement.

