from flask import Flask, render_template, request
import os
import smtplib
import secrets
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

email2 = os.getenv('email2')
key = os.getenv('email2_key')
email1 = os.getenv('email1')


# print(f'email1={email1}, email2={email2}')


def send_mail(message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email2, password=key)
        connection.sendmail(from_addr=email2, to_addrs=email1,
                            msg=f"Subject:Hello\n\n{message}")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        print(f'request is POST')

        data = request.form
        message = f'Name: {data["name"]}\nEmail: {data["email"]}\nPhone: {data["phone"]}\nMessage:\n{data["message"]}'
        send_mail(message)
        return render_template('index.html', is_sent=True)

    return render_template('index.html', is_sent=False)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
