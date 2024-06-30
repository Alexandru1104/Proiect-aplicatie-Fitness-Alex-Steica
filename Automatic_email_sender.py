
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
import Data_base.Sign_up_and_login as login_utils
import User_info


def send_mail(
    sender_gmail: str,
    sender_password: str,
    to_address: str,
    body: str,
    subject: str,
):
    message = MIMEMultipart() 
    message["From"] = sender_gmail
    message["To"] = to_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with SMTP("smtp.gmail.com", 587) as server:
        server.starttls() 
        server.login(sender_gmail, sender_password)
        server.sendmail(sender_gmail, to_address, message.as_string()) 
        print(f"E-mail successfully sent to {to_address} !")


if __name__ == "__main__":
    # password = open("mail_pass.txt", "r").read()
    password = "Fitnessapp04"

    send_mail(
        sender_gmail="fitnessapp@gmail.com",
        sender_password=password,
        to_address= "alexsteica92@yahoo.com",
        # to_address= User_info.get_current_usr().get_email_variable(),
        body="You have been successfully logged in on the Fitness App !",
        subject="Autentification completed !! "
    )


