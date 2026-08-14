import re
import telebot

# ከ BotFather የተቀበሉትን ቦት ቶከን እዚህ ያስገቡ
TOKEN = "8904195446:AAHJhR7F5-9psn-Z5PZiZBxgCxCPzOBDCwY"

bot = telebot.TeleBot(TOKEN)

# የየተጠቃሚውን አጠቃላይ ድምር (Total) በጊዜያዊነት ለመያዝ የሚያገለግል
user_totals = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.chat.id
    if user_id not in user_totals:
        user_totals[user_id] = 0
        
    welcome_text = (
        "ሰላም! 👋 እኔ የሂሳብ ድምር ማስያ ቦት ነኝ።\n\n"
        "📌 **እንዴት እንደሚሰራ:**\n"
        "• የትኛውንም ቁጥር ወይም የቁጥሮች ዝርዝር ይላኩልኝ (ምሳሌ፡ `150` ወይም `100 + 250.50 + 50`)\n"
        "• በፅሁፍ ውስጥ ያሉትን ቁጥሮች ለይቼ በራሴ እደምርልዎታለሁ።\n\n"
        "⚙️ **ትዕዛዞች:**\n"
        "/total - እስከ አሁን የተደመረውን አጠቃላይ ድምር ለማየት\n"
        "/reset - ድምሩን ወደ ዜሮ (0) ለመመለስ\n"
        "/help - መመሪያ ለማየት"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['reset'])
def reset_total(message):
    user_id = message.chat.id
    user_totals[user_id] = 0
    bot.reply_to(message, "🔄 አጠቃላይ ድምርዎ ወደ **0** ተመልሷል!", parse_mode="Markdown")

@bot.message_handler(commands=['total'])
def show_total(message):
    user_id = message.chat.id
    total = user_totals.get(user_id, 0)
    bot.reply_to(message, f"📊 **እስከ አሁን ያለው አጠቃላይ ድምር:** `{total:,.2f} ብር`", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def calculate_sum(message):
    user_id = message.chat.id

    # በፅሁፉ ውስጥ ያሉትን ኢንቲጀር እና ዴሲማል ቁጥሮች በሙሉ መለየት
    numbers = re.findall(r'[-+]?\d*\.?\d+', message.text)

    # ቁጥር ከሌለ ምንም አያደርግም
    if not numbers:
        return

    # ቁጥሮቹን ወደ float መቀየር (ባዶ ወይም ነጥብ ብቻ የሆኑትን በማስወገድ)
    floated_numbers = []
    for n in numbers:
        try:
            floated_numbers.append(float(n))
        except ValueError:
            continue

    if not floated_numbers:
        return

    current_sum = sum(floated_numbers)

    # የተጠቃሚውን አጠቃላይ ድምር ማዘመን
    user_totals[user_id] = user_totals.get(user_id, 0) + current_sum

    # የተቀበላቸውን ቁጥሮች በ ' + ' አያይዞ ማሳየት
    nums_str = " + ".join([f"{n:g}" for n in floated_numbers])
    
    response = (
        f"➕ **የተላኩት ቁጥሮች ድምር:** `{nums_str}` = **{current_sum:,.2f}**\n"
        f"💰 **የአጠቃላይ ሂሳብ ድምር (Total):** `{user_totals[user_id]:,.2f} ብር`"
    )

    bot.reply_to(message, response, parse_mode="Markdown")

print("ቦቱ መስራት ጀምሯል...")
bot.infinity_polling()