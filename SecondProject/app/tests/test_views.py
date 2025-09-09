from django.urls import reverse
from django.core import mail


def test_an_admin_view(admin_client):
    url = reverse("admin:index")
    response = admin_client.get(url, secure=True)
    assert response.status_code == 200


def test_new_user(django_user_model):
    response = django_user_model.objects.create_user(
        username="test_user", password="1234"
    )
    assert response.is_authenticated


def test_send_mail(mailoutbox):
    mail.send_mail("subject", "body", "from@example.com", ["to@example.com"])
    assert len(mail.outbox) == 1
    m = mail.outbox[0]
    assert m.subject == "subject"
    assert m.body == "body"
    assert m.from_email == "from@example.com"
    assert m.to == ["to@example.com"]
