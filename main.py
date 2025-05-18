

# Hello My name is Michael(Rustambek) this is masterpiece. Telegran @MikeeSc . Ko'rishganda Ko'rishguncha Hogwarts
# And most importantly I hope I will be selected and be given a full grant. CIA for now


import json
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


with open('data_updated.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = [item["question"] for item in data]
answers = [item["answer"] for item in data]
topics = sorted(set(item["topic"] for item in data))
topic_question_map = {t: [] for t in topics}
for item in data:
    topic_question_map[item["topic"]].append((item["question"], item["answer"], item.get("section", "")))

vectorizer = TfidfVectorizer().fit(questions)
question_vectors = vectorizer.transform(questions)

TELEGRAM_TOKEN = "7981347726:AAFp-vvy2BIugdB7OpVUgG70q17M2k3wl5E"

logging.basicConfig(level=logging.INFO)


async def send_main_menu(chat_or_query):
    keyboard = [
        [InlineKeyboardButton("📚 Topics", callback_data="menu_topics")],
        [InlineKeyboardButton("📊 Stats", callback_data="menu_stats")],
        [InlineKeyboardButton("🧠 Fun Fact", callback_data="menu_fact")],
        [InlineKeyboardButton("💬 Ask a Question", callback_data="menu_ask")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Welcome to HogwartsBot 🧙‍♂️✨\nChoose an option below:"
    if hasattr(chat_or_query, 'message'):
        await chat_or_query.message.reply_text(text, reply_markup=reply_markup)
    else:
        await chat_or_query.edit_message_text(text, reply_markup=reply_markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_main_menu(update)


async def handle_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == "menu_topics":
        keyboard = [[InlineKeyboardButton(t, callback_data=f"topic::{t}")] for t in topics]
        keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_back")])
        await query.edit_message_text("Choose a topic:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == "menu_stats":
        msg = "📊 *HogwartsBot Stats*:\n• 4 total cohorts held\n• Max 200 participants\n• Online + offline learning\n• Estimated $87 per participant"
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_back")]]
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == "menu_fact":
        facts = [item for item in data if item["topic"] == "Random Fact"]
        fact = random.choice(facts)
        msg = f"🧠 *Fun Fact:*\n{fact['answer']}"
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_back")]]
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == "menu_ask":
        await query.edit_message_text("Type your question now 👇")

    elif action == "menu_back":
        await send_main_menu(query)


async def handle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    topic = query.data.split("::")[1]
    buttons = [[InlineKeyboardButton(q[0], callback_data=f"question::{q[0]}")] for q in topic_question_map[topic]]
    buttons.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_back")])
    markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(f"📚 Questions in *{topic}*:", parse_mode="Markdown", reply_markup=markup)

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    question_text = query.data.split("::")[1]
    for item in data:
        if item["question"] == question_text:
            section = item.get("section", "Unknown")
            answer = f"❓ {item['question']}\n💬 {item['answer']}\n📌 Source: *{section}*"
            break
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_back")]]
    await query.edit_message_text(answer, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    user_vector = vectorizer.transform([user_question])
    similarity_scores = cosine_similarity(user_vector, question_vectors)
    best_idx = similarity_scores.argmax()
    best_score = similarity_scores[0][best_idx]
    reply = "❗ Sorry, I couldn't find an answer in the document."
    if best_score > 0.4:
        section = data[best_idx].get("section", "Unknown")
        reply = f"❓ {data[best_idx]['question']}\n💬 {data[best_idx]['answer']}\n📌 Source: *{section}*"
    await update.message.reply_text(reply, parse_mode="Markdown")


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_menu_click, pattern="^menu_"))
    app.add_handler(CallbackQueryHandler(handle_topic, pattern="^topic::"))
    app.add_handler(CallbackQueryHandler(handle_question, pattern="^question::"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
