import pandas as pd
from sklearn.linear_model import LogisticRegression
from datetime import date
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

print("\n=== BURNOUT & STRESS ANALYSIS SYSTEM (AUTOMATED) ===")

df = pd.read_csv(
    r"C:\Users\HP 745 G6\Desktop\burnout ML Project\training_data.csv")

X = df[["WorkingHours", "SleepHours"]]
y = df["Burnout"]

model = LogisticRegression()
model.fit(X, y)

receiver_email = input("Enter receiver email: ")
interval_min = int(input("Enter interval between mails (in minutes): "))

scheduled_inputs = []

print("\nEnter future burnout inputs (type 'done' to finish):")
while True:
    work = input("Working hours (or 'done'): ")
    if work.lower() == "done":
        break
    sleep = input("Sleep hours: ")

    scheduled_inputs.append({
        "work": int(work),
        "sleep": int(sleep)
    })

print(f"\n✅ {len(scheduled_inputs)} inputs stored successfully!")
print("📡 Automation started...\n")

def get_suggestions(work, sleep):
    if work >= 10 and sleep <= 5:
        return "High", [
            "Reduce working hours",
            "Sleep at least 7 hours",
            "Avoid overtime",
            "Take mental breaks"
        ]
    elif work >= 8:
        return "Medium", [
            "Maintain work-life balance",
            "Avoid late nights"
        ]
    else:
        return "Low", ["You are following a healthy routine"]

def burnout_risk(model, work, sleep):
    person = pd.DataFrame([[work, sleep]],
                          columns=["WorkingHours", "SleepHours"])
    return round(model.predict_proba(person)[0][1] * 100, 2)

def ask_reason():
    print("\nWhy do you think burnout is high?")
    reasons = {
        1: "Too many working hours",
        2: "Not enough sleep",
        3: "Too many deadlines",
        4: "No proper breaks"
    }
    for k, v in reasons.items():
        print(f"{k}. {v}")
    print("5. None")

    choice = int(input("Choose reason: "))

    return {
        1: ["Reduce work hours", "Delegate tasks"],
        2: ["Sleep 7+ hours", "Avoid late nights"],
        3: ["Split tasks", "Set realistic deadlines"],
        4: ["Take short breaks", "Relax your mind"]
    }.get(choice, ["Maintain balanced routine"])

def send_email(receiver, stress, trend, suggestions):
    sender_email = "pavankalyankaturi2803@gmail.com"
    app_password = "ctfo wvli kecm hlan"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver
    msg["Subject"] = "Burnout Trend Update"

    body = f"""
Hello,

Stress Level: {stress}
Burnout Trend: {trend}

Suggestions:
"""
    for s in suggestions:
        body += f"- {s}\n"

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()

    print("📧 Email sent successfully")

os.makedirs("data", exist_ok=True)
history_file = "data/burnout_history.xlsx"
previous_risk = None

for i, entry in enumerate(scheduled_inputs):
    print(f"\n--- Trigger {i+1} ---")

    work = entry["work"]
    sleep = entry["sleep"]

    current_risk = burnout_risk(model, work, sleep)
    stress, default_suggestions = get_suggestions(work, sleep)

    if previous_risk is None:
        trend = f"Initial Measurement ({current_risk}%)"
    elif current_risk > previous_risk:
        trend = f"Burnout INCREASED ⬆️ ({current_risk}%)"
    elif current_risk < previous_risk:
        trend = f"Burnout DECREASED ⬇️ ({current_risk}%)"
    else:
        trend = f"No Change ({current_risk}%)"

    if stress == "High":
        suggestions = ask_reason()
    else:
        suggestions = default_suggestions

    # Save history
    entry_df = pd.DataFrame([[date.today(), current_risk, trend]],
                            columns=["Date", "BurnoutRisk", "Trend"])
    if os.path.exists(history_file):
        old = pd.read_excel(history_file)
        history_df = pd.concat([old, entry_df], ignore_index=True)
    else:
        history_df = entry_df
    history_df.to_excel(history_file, index=False)

    send_email(receiver_email, stress, trend, suggestions)
    previous_risk = current_risk

    if i < len(scheduled_inputs) - 1:
        print(f"⏱ Waiting {interval_min} minute(s)...\n")
        time.sleep(interval_min * 60)

print("\n✅ AUTOMATION COMPLETED SUCCESSFULLY!")
