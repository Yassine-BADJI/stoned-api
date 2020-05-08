from sendgrid import SendGridAPIClient

from config import sg_key


def send_mail(message):
    sg = SendGridAPIClient(sg_key)
    sg.send(message)
