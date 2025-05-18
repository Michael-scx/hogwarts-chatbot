# 🧙 Hogwarts Summer School - Telegram Chatbot

This is a fully functional, created by Michael Telegram chatbot designed for the **Hogwarts Summer of Research** case study for New Uzbekistan University. It helps users explore structured information about the summer school program and provides instant, document-grounded answers.

---

## 📌 Features

✅ **Data-Grounded Q&A:**  
Answers user questions only from the provided [Google Doc](https://docs.google.com/document/d/1PmXpxXUvaAMN_hnCxNfrh8o3fUu0hVQSg3VKsWR0k7Y) — no hallucinations or extra info.

✅ **Interactive Menu UI:**  
A clean inline button menu lets users explore topics, stats, or ask questions easily.

✅ **Topic-Based Navigation (/topics):**  
Structured buttons by categories like Timeline, Eligibility, Budget, and more.

✅ **Smart Question Matching:**  
Uses TF-IDF to respond to any user-typed questions with the closest match from the dataset.

✅ **Source Justification:**  
Each answer includes a “Source” label referencing its original section in the document.

✅ **Fun & Stats Commands:**  
• `/fact` – Show a fun random fact  
• `/stats` – Display key project statistics

---

## 🗂 Project Structure

```
├── main.py                # Main Telegram bot logic
├── data_updated.json      # Structured Q&A with topics + sources
├── requirements.txt       # Install dependencies
```

---

## ▶️ How to Run

### 1. Clone or download this repo

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Telegram bot token
In `main.py`, replace the value of `TELEGRAM_TOKEN` with your own token from [@BotFather](https://t.me/BotFather)

### 4. Start the bot
```bash
python main.py
```

---

## 🧠 Written Explanation (for Google Form)

**a. Architecture overview:**  
Used JSON for data storage. TF-IDF with `scikit-learn` powers smart matching. Telegram bot built with `python-telegram-bot`. Commands and inline buttons control user flow.

**b. Main functionalities and limitations:**  
Bot answers only from the official doc. Supports structured categories, random facts, and statistics. Doesn’t support multiple languages in this version.

**c. How I validated answers:**  
All Q&A were directly extracted and tagged with source sections. Bot was tested to ensure zero hallucination using similarity thresholds.

---

## 🤝 Acknowledgements

- Hogwarts Summer School Team @ NewUU
- OpenAI, Google Docs, and Telegram Bot API

---

*Built by Rustambek Yuldashaliyev(Michael) 🇺🇿*
