from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres import constraints
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    ArrayField,
    HStoreField,
    CICharField,
    JSONField,
    RangeOperators,
)
from django.contrib.postgres.indexes import GistIndex
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.utils import timezone
from django.core.validators import EmailValidator


class BbManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("price")


class RubricManager(models.Manager):
    def get_queryset(self):
        return RubricQuerySet(self.model, using=self._db)

    def order_by_bb_count(self):
        return self.get_queryset().order_by_bb_count()


class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return self.annotate(cnt=models.Count("entries")).order_by("-cnt")


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Note(models.Model):
    content = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")


class SuperRubric(models.Model):
    title = models.CharField(max_length=50, blank=True)


class Rubric(models.Model):
    name = models.CharField(max_length=50, blank=True)
    show = models.BooleanField(default=False)
    order = models.SmallIntegerField(default=0, db_index=True)
    super_rubric = models.ForeignKey(
        SuperRubric,
        related_name="super_rubric",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    objects = RubricQuerySet.as_manager()

    class Meta:
        db_table = "rubric"
        ordering = "order", "name"

    def __str__(self):
        return self.name

    @staticmethod
    def get_first_rubric():
        return Rubric.objects.first()


class Bb(TimeStampedModel):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True, default=None)
    price = models.IntegerField(blank=True, null=True)
    objects = models.Manager()
    by_price = BbManager()
    rubric = models.ForeignKey(
        Rubric,
        on_delete=models.PROTECT,
        null=True,
        default=None,
        related_name="entries",
    )

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
        choices=IntegerKinds.choices, default=IntegerKinds.SELL, blank=True
    )

    def __str__(self):
        if self.rubric:
            return "%s %s %s %s" % (
                self.title,
                self.content,
                self.price,
                self.rubric.name,
            )
        else:
            return "%s %s" % (self.title, self.price)


class Measure(models.Model):
    class Measurements(float, models.Choices):
        METERS = 1.0, "METERS"
        FEET = 0.3048, "FEET"
        YARDS = 0.9144, "YARDS"

    measurement = models.FloatField(choices=Measurements.choices)


class Board(models.Model):
    title = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(blank=True, null=True)
    rubric = models.ForeignKey(
        Rubric,
        on_delete=models.SET(Rubric.get_first_rubric),
        limit_choices_to={"show": True},
        # related_name="+",
        related_query_name="entry",
    )

    class Meta:
        order_with_respect_to = "rubric"

    def get_bbs(self):
        return self.rubric.entry.all()

    @staticmethod
    def get_home_rubrics():
        return Rubric.objects.filter(entry__title="Home")


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(
        blank=True, validators=[EmailValidator(message="Invalid email")]
    )


class Spare(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(
        Spare, through="Kit", through_fields=("machine", "spare")
    )

    notes = GenericRelation("Note")

    def clean(self):
        errors = {}
        if not self.name:
            errors["name"] = ValidationError("Укажите название")

    def __str__(self):
        return self.name


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return self.machine.name + " + " + self.spare.name


class Magazine(models.Model):
    title = models.CharField(
        max_length=30, error_messages={"invalid": "Incorrectly name"}
    )
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


class Message(models.Model):
    content = models.TextField()


class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Message1(models.Model):
    content = models.TextField()
    name = models.CharField()
    email = models.EmailField()

    class Meta:
        abstract = True


class PrivateMessage1(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    email = None


class RevRubric(Rubric):
    class Meta:
        proxy = True
        ordering = ["-name"]


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    bb = models.ForeignKey(
        Bb, null=True, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} оставил {self.comment} in {self.bb}"


class PGSRoomReserving(models.Model):
    name = models.CharField(max_length=20, verbose_name="Помещение")
    reserving = DateTimeRangeField(verbose_name="Время резервирования")
    cancelled = models.BooleanField(
        default=False, verbose_name="Отменить резервирование"
    )

    class Meta:
        indexes = [
            GistIndex(
                fields=["name", "reserving"],
                name="i_pgsrr_reserving",
                opclasses=(
                    "gist_trgm_ops",
                    "range_ops",
                ),
                fillfactor=50,
            )
        ]
        constraints = [
            ExclusionConstraint(
                name="c_pgsrr_reserving",
                expressions=[
                    ("name", RangeOperators.EQUAL),
                    ("reserving", RangeOperators.EQUAL),
                ],
                condition=models.Q(cancelled=False),
            )
        ]

    def __str__(self):
        return self.name


class PGSRubric(models.Model):
    name = models.CharField(max_length=20, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    tags = ArrayField(base_field=models.CharField(max_length=20), verbose_name="Теги")

    class Meta:
        indexes = [
            models.Index(
                fields=("name", "description"),
                name="i_pgsrubric_name_description",
                opclasses=(
                    "gist_trgm_ops",
                    "gist_trgm_ops",
                ),
            )
        ]
        constraints = [
            ExclusionConstraint(
                name="c_pgsrubric_name_description",
                expressions=[
                    ("name", RangeOperators.EQUAL),
                    ("description", RangeOperators.EQUAL),
                ],
            )
        ]


class PGSProject2(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название")
    platforms = HStoreField(verbose_name="Использование платформы")
