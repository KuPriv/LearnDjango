from django.db import models
from django.contrib.auth.models import User


class Bb(models.Model):
    KINDS = (
        ("b", "buy"),
        ("s", "sell"),
        ("t", "trade"),
    )
    kind = models.CharField(max_length=1, choices=KINDS, blank=True)

    class TextKinds(models.TextChoices):
        BUY = "b", "Buy"
        SELL = "s", "Sell"
        TRADE = "t", "Trade"
        __empty__ = "Choose type of published announcement"

    kind2 = models.CharField(max_length=1, choices=TextKinds.choices, blank=True)

    class IntegerKinds(models.IntegerChoices):
        BUY = 1, "Buy"
        SELL = 2, "Sell"
        TRADE = 3, "Trade"

    kind3 = models.SmallIntegerField(
        choices=IntegerKinds.choices, default=IntegerKinds.SELL
    )


class Measure(models.Model):
    class Measurements(float, models.Choices):
        METERS = 1.0, "METERS"
        FEET = 0.3048, "FEET"
        YARDS = 0.9144, "YARDS"

    measurement = models.FloatField(choices=Measurements.choices)


class Rubric(models.Model):
    show = models.BooleanField(default=False)

    class Meta:
        db_table = "rubric"

    @staticmethod
    def get_first_rubric():
        return Rubric.objects.first()


class Board(models.Model):

    rubric = models.ForeignKey(
        Rubric,
        on_delete=models.SET(Rubric.get_first_rubric),
        limit_choices_to={"show": True},
        related_name="+",
        related_query_name="entry",
    )

    def get_bbs(self):
        return self.rubric.entry.all()

    @staticmethod
    def get_home_rubrics():
        return Rubric.objects.filter(entry__title="Home")


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Spare(models.Model):
    name = models.CharField(max_length=30)


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)


class Magazine(models.Model):
    title = models.CharField(max_length=30)
    published = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0)
    rubric = models.ForeignKey("Rubric", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-published", "title"]
        unique_together = (
            ("title", "published"),
            ("title", "price"),
        )
        get_latest_by = "published"
        indexes = [
            models.Index(
                fields=["title"],
                name="%(app_label)s_%(class)s_main",
                condition=models.Q(price__lte=1000),
            )
        ]
