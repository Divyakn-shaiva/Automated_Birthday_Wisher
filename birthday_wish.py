import mysql.connector
import datetime as dt
import smtplib
import random
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ------------------- Configuration -------------------

EMAIL_ADDRESS = 'cseaimlbday@gmail.com'
EMAIL_PASSWORD = 'zswqyffytgjdbhjs'  # Use your Gmail App Password (no spaces)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'b_day'
}

LOG_FILE = 'birthday_log.txt'

# ------------------- Setup Logging -------------------

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ------------------- Birthday Messages -------------------

BIRTHDAY_MESSAGES = [
    """🎈🎂 Hey {name}! 🎂🎈

Wishing you a fantastic birthday filled with laughter, joy, and unforgettable moments! 🥳
May your day be as wonderful as you are, and your year be full of success and happiness. 🌟🎁

Enjoy your special day to the fullest! 🎊🎉

Warm wishes,  
🎓 CSE AI&ML Team 💻
""",
    """🎉 Happy Birthday, {name}! 🎉

Hope your birthday is as amazing as your smile 😊
Keep dreaming big and achieving great things! 💡🚀
Let today be the beginning of a beautiful year full of happiness and success! 🌼✨

Lots of love from all of us,  
🎓 Your CSE AI&ML Family 💖
""",
    """🌟 Dear {name}, 🌟

Happy Birthday! May this special day bring you happiness, knowledge, and endless opportunities.
Keep dreaming big and achieving great things! 💡🚀
Enjoy your special day to the fullest! 🎊🎉

Wishing you the best from all of us 🍰☀️🎁  
Celebrate BIG and stay awesome 🎈🎉

📚 CSE(AI&ML) Team
""",
    """🥳 {name}, it’s your special day! 🥳

Happy Birthday! May your day be as wonderful as your efforts and as inspiring as your goals.
Let today be the beginning of a beautiful year full of happiness and success! 🌼✨
Here’s to another year of greatness!

Happy birthday once again! 🎂💙  
From your CSE AI&ML family 👩‍💻👨‍💻
"""
]

# ------------------- Send Email Function -------------------

def send_email(to_email: str, name: str):
    subject = f"🎉 Happy Birthday, {name}! 🎂"
    message_body = random.choice(BIRTHDAY_MESSAGES).format(name=name)

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        logging.info(f"✅ Email sent to {name} ({to_email})")
        print(f"✅ Email sent to {name} ({to_email})")
    except Exception as e:
        logging.error(f"❌ Failed to send email to {name} ({to_email}). Error: {e}")
        print(f"❌ Failed to send email to {name} ({to_email}). Error: {e}")

# ------------------- Main Birthday Logic -------------------

def send_birthday_wishes():
    today = dt.datetime.now().strftime('%m-%d')
    found = False

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT name, email, DATE_FORMAT(dob, '%m-%d') as bday FROM student"
        cursor.execute(query)
        students = cursor.fetchall()

        for name, email, bday in students:
            if bday == today:
                send_email(email, name)
                found = True

        if not found:
            msg = "📅 No birthdays today."
            logging.info(msg)
            print(msg)

    except mysql.connector.Error as err:
        logging.error(f"❌ Database Error: {err}")
        print(f"❌ Database Error: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# ------------------- Entry Point -------------------

if __name__ == "__main__":
    send_birthday_wishes()
