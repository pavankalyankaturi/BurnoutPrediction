from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LogisticRegression
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ================= LOAD & TRAIN MODEL =================
df = pd.read_csv(
    r"C:\Users\HP 745 G6\Desktop\burnout ML Project\training_data.csv"
)

X = df[["WorkingHours", "SleepHours"]]
y = df["Burnout"]

model = LogisticRegression()
model.fit(X, y)

# ================= HELPER FUNCTIONS =================
def burnout_risk(work, sleep):
    person = pd.DataFrame(
        [[work, sleep]],
        columns=["WorkingHours", "SleepHours"]
    )
    return round(model.predict_proba(person)[0][1] * 100, 2)

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
        return "Low", [
            "You are following a healthy routine"
        ]

def send_email(receiver, stress, risk, suggestions):
    sender_email = "pavankalyankaturi2803@gmail.com"
    app_password = "ctfo wvli kecm hlan"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver
    msg["Subject"] = "Burnout Analysis Report"

    body = f"""
Hello,

Burnout Risk: {risk}%
Stress Level: {stress}

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

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    # ----- HANDLE BOTH GET & POST -----
    if request.method == "POST":
        work = int(request.form["work"])
        sleep = int(request.form["sleep"])
        receiver = request.form["email"]
    else:
        work = int(request.args.get("work"))
        sleep = int(request.args.get("sleep"))
        receiver = request.args.get("email")

    risk = burnout_risk(work, sleep)
    stress, suggestions = get_suggestions(work, sleep)

    send_email(receiver, stress, risk, suggestions)

    return render_template(
        "result.html",
        risk=risk,
        stress=stress,
        suggestions=suggestions
    )

if __name__ == "__main__":
    app.run(debug=True)
