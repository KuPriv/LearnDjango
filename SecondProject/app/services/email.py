from django.core.mail import (
    EmailMessage,
    get_connection,
    EmailMultiAlternatives,
    send_mail,
    send_mass_mail,
)
from django.template.loader import render_to_string
from django.contrib.auth.models import User

em = EmailMessage(
    subject="Ваш новый пароль",
    body="Ваш новый пароль находится во вложении",
    attachments=[("password.txt", "12345678", "text/plain")],
    to=["sezen.egor@mail.ru"],
)
em.send()

em = EmailMessage(
    subject="Запрошенный файл",
    body="Получите запрошенный файл",
    to=["sezen.egor@mail.ru"],
)
em.attach_file(
    r"C:\Users\sezen\Desktop\Python Projects\LearnDjango\SecondProject\media\uploads\2026_02_19_15_38_15_ed418ec152904f3997fc421db418b2e7.jpg"
)
em.send()

context = {"user": "Вася пупкин"}
s = render_to_string("email/letter.txt", context)
em = EmailMessage(subject="Оповещение", body=s, to=["sezen.egor@mail.ru"])
em.send()

con = get_connection()
con.open()
email1 = EmailMessage(..., connection=con)
email1.send()
email2 = EmailMessage(..., connection=con)
email2.send()
con.close()

con = get_connection()
email1 = EmailMessage(..., connection=con)
email2 = EmailMessage(..., connection=con)
email3 = EmailMessage(..., connection=con)
con.send_messages([email1, email2, email3])
con.close()

em = EmailMultiAlternatives(subject="Test", body="Teest", to=["sezen.egor@mail.ru"])
em.attach_alternative("<h1>Test</h1>", "text/html")
em.send()

send_mail(
    "Test",
    "Test!!!",
    "super.goremo@gmail.com",
    ["sezen.egor@mail.ru"],
    html_message="<h1>Test</h1>",
)

msg1 = (
    "Подписка",
    "Подтвердите",
    "super.goremore@gmail.com",
    ["user1@mail.ru", "user2@mail.ru"],
)
msg2 = ("Подписка", "Подтверждена", "super.goremore@gmail.com", ["user@mail.ru"])
send_mass_mail(msg1, msg2)

user = User.objects.get(username="admin")
user.email_user("Подъем!", "Admin, не спи", fail_silently=True)
