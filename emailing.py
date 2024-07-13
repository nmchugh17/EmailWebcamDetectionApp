import smtplib
import imghdr
import os
from email.message import EmailMessage

HOST = "smtp.gmail.com"
PORT = 587
SENDER = "nmchu17@gmail.com"
RECEIVER = "nmchu17@gmail.com"
PASSWORD = os.getenv("PASSWORD")


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hi 5")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP(HOST, PORT)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(image_path="images/19.png")
