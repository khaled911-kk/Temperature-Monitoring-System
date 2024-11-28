import random
import time
import sqlite3
import smtplib
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# إعداد قاعدة البيانات
def setup_database():
    conn = sqlite3.connect('temperature_monitor.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS temperature_logs
                 (timestamp TEXT, temperature REAL)''')
    conn.commit()
    conn.close()

# محاكاة درجة الحرارة
def simulate_temperature():
    return random.uniform(20, 40)  # درجات حرارة بين 20 و 40

# التحقق من درجة الحرارة وإرسال البريد الإلكتروني إذا لزم الأمر
def check_temperature(temp):
    if temp > 30:
        send_email_alert("High Temperature Alert", f"Warning: Temperature exceeded 30°C. Current temperature: {temp:.2f}°C")
        return f"Warning! High temperature: {temp}°C"
    else:
        return f"Temperature is normal: {temp}°C"

# إرسال تنبيه بالبريد الإلكتروني
def send_email_alert(subject, body):
    sender = "your_email@example.com"
    recipient = "recipient_email@example.com"
    password = "your_email_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# تخزين البيانات في قاعدة البيانات
def log_data_to_db(temp):
    conn = sqlite3.connect('temperature_monitor.db')
    c = conn.cursor()
    c.execute("INSERT INTO temperature_logs (timestamp, temperature) VALUES (CURRENT_TIMESTAMP, ?)", (temp,))
    conn.commit()
    conn.close()

# عرض البيانات بيانيًا باستخدام matplotlib
def plot_temperature_data():
    conn = sqlite3.connect('temperature_monitor.db')
    query = "SELECT * FROM temperature_logs"
    data = pd.read_sql(query, conn)
    conn.close()

    data['timestamp'] = pd.to_datetime(data['timestamp'])
    plt.plot(data['timestamp'], data['temperature'], label="Temperature")
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Monitoring')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

# تحديث واجهة المستخدم
def update_ui(temp):
    window = tk.Tk()
    window.title("Temperature Monitoring System")

    # Label for current temperature
    temp_label = tk.Label(window, text=f"Current Temperature: {temp:.2f}°C", font=("Arial", 14))
    temp_label.pack(pady=20)

    # Check for alerts
    if temp > 30:
        messagebox.showwarning("Alert", f"High temperature detected: {temp:.2f}°C")

    # Button to plot temperature data
    plot_button = tk.Button(window, text="Show Temperature Graph", command=plot_temperature_data)
    plot_button.pack(pady=10)

    window.mainloop()

# بدء النظام
def monitor_system():
    setup_database()  # إعداد قاعدة البيانات عند بدء النظام
    while True:
        temperature = simulate_temperature()
        print(check_temperature(temperature))  # إظهار التنبيه
        log_data_to_db(temperature)  # تخزين البيانات في قاعدة البيانات
        update_ui(temperature)  # تحديث واجهة المستخدم
        time.sleep(5)  # تأخير لمدة 5 ثواني قبل المحاكاة التالية

# بدء مراقبة النظام
monitor_system()
