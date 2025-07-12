import logging

from django.db.models import (
    F,
    Q,
    Min,
    Max,
    Count,
    Avg,
    Sum,
    IntegerField,
    Value,
    ExpressionWrapper,
    CharField,
)
from django.http import HttpResponse
from django.db.models.functions import Concat, Coalesce, Greatest, Least, Cast, StrIndex

from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the app index.")


def show_rubric(request):
    r = Rubric()
    r.name = "техника"
    r.save()
    return HttpResponse(r.name)


def show_measurement(request):
    m = Measure()
    m.measurement = Measure.Measurements.FEET
    return HttpResponse(m.measurement)


def set_announcement(request):
    r = Rubric.objects.get(name="Мебель")
    b = Bb.objects.create(title="Дивуан", content="Пропуканный", price=999999, rubric=r)

    return HttpResponse(b)


def show_board(request):
    r = Rubric.objects.get(name="Мебель")
    print(r.get_board_order())
    print(r.set_board_order([3, 2, 1]))
    return HttpResponse(", ".join(str(obj) for obj in r.get_board_order()))


def OneToOne(request):
    u = User.objects.get(username="admin")
    au, create_flag = AdvUser.objects.get_or_create(user=u)
    u.save()
    return HttpResponse("%s , %s" % (au.user, u.advuser))


def ManyToMany(request):
    s1 = Spare.objects.create(name="Болт")
    s2 = Spare.objects.create(name="Гайка")
    s3 = Spare.objects.create(name="Винтик")
    m1 = Machine.objects.create(name="SameAsWell")
    m2 = Machine.objects.create(name="Говновоз")
    m1.spares.add(s1, s2)
    m1.spares.add(s3)
    s1.machine_set.all()
    return HttpResponse(m1.spares.all())


def try_bulk_create(request):
    r = Rubric.objects.get(name="Мяу")
    if (
        Bb.objects.filter(title="Палясос").exists()
        and Bb.objects.filter(title="Насосоос").exists()
    ):
        pass
    else:
        Bb.objects.bulk_create(
            [
                Bb(title="Палясос", content="Не гав", price=111, rubric=r),
                Bb(title="Насосоос", content="Му", price=999, rubric=r),
            ]
        )
    Bb.objects.filter(price__lt=150).update(price=150)
    print(Bb, r)
    return HttpResponse(Bb.objects.all())


def try_bulk_update(request):
    if (
        Bb.objects.filter(title="Дача").exists()
        and Bb.objects.filter(title="Диван").exists()
    ):
        pass
    else:
        Bb.objects.bulk_create(
            [Bb(title="Дача", price=555), Bb(title="Диван", price=9999)]
        )

    b1 = Bb.objects.get(title="Дача")
    b2 = Bb.objects.get(title="Диван")
    b1.price = 100000
    b2.price = 999
    Bb.objects.bulk_update((b1, b2), ("price",))
    print(b1.price, b2.price)
    return HttpResponse(str(b1.price) + "///" + str(b2.price) + str(b1))


def clear_bb_content(request):
    Bb.objects.filter(content=None).delete()
    return HttpResponse(Bb)


def check_full_clean(request):
    # Валидация модели
    b = Bb()
    b.full_clean()
    return HttpResponse(" ")


def just_print_results(request):
    b = Bb.objects.all()
    b_cor = Bb.objects.get(title="Палясос")
    b_cor.kind = "s"
    b_cor.kind2 = "b"
    b_cor.save()
    print(b_cor.get_kind_display())
    print(b_cor)
    m = Measure.objects.first()
    print(m.measurement)
    print(m.get_measurement_display())

    return HttpResponse(b_cor)


def access_to_related_records(request):
    # связь один ко многим
    print("ONE-TO-MANY")
    r = Rubric.objects.get(name="Мяу")
    print("all ->")
    # for bb in r.bb_set.all():
    for bb in r.entries.all():
        print(bb)
    print("filter ->")
    # for bb in r.bb_set.filter(price__lt=1000):
    for bb in r.entries.filter(price__lt=1000).distinct():
        print(bb)
    # entries - задаем имя в related_name в models.py

    # связь один к одному
    print("ONE-TO-ONE")
    au = AdvUser.objects.first()
    print(au.user, au.user.username)
    u = User.objects.first()
    print(f"{u.advuser = }")

    # связь многие со многими
    print("MANY-TO-MANY")
    m = Machine.objects.get(pk=11)
    print(m.name)
    for s in m.spares.all():
        print(s.name)

    s = Spare.objects.get(name="Винтик")
    for m in s.machines.all():
        print(m.name)

    """s2 = Spare.objects.get(name="Гайка")
    for m in s2.machine_set.all():
        print(m.name)"""

    return HttpResponse(" ")


def check_other_functions(request):
    s = ""
    for r in Rubric.objects.all():
        s += r.name + " "
        logging.warning(r.name)

    print("//////////////")
    r = Rubric.objects.get(name="Мяу")
    for bb in r.entries.all():
        logging.warning(bb.title)
    print("///////////")
    # тк есть get_latest_by можно вызвать без параметров
    m = Magazine.objects.earliest()
    logging.warning(m.title)
    logging.warning(Magazine.objects.latest().title)
    logging.warning(Bb.objects.all()[0].pk)
    r = Rubric.objects.get(name="Мебель")
    logging.warning(r.board_set.all()[0].pk)
    b1 = r.board_set.get(pk=2)
    logging.warning("%s %s " % (b1.pk, b1.title))
    b2 = b1.get_previous_in_order()
    logging.warning("%s %s " % (b2.pk, b2.title))
    logging.warning(Bb.objects.count())
    print("////////////////////")
    m = Magazine.objects.get(pk=1)
    logging.warning(m.title)
    m2 = m.get_next_by_published()
    logging.warning(m2.title)
    m3 = m.get_next_by_published(price__lt=555)
    logging.warning(m3.title)
    logging.warning(m2.get_previous_by_published().title)
    print("///////////////")
    for b in Bb.objects.exclude(price__gte=554):
        logging.warning(b.title)

    r = Rubric.objects.get(pk=10)
    for b in Bb.objects.filter(rubric=r, price__gte=444):
        logging.warning(b.title)
    print("//////////")
    for m in Magazine.objects.filter(published__week_day=6):
        logging.warning("%s %s " % (m.title, m.published))
    print("--------")
    for m in Magazine.objects.filter(published__year__lte=2025):
        logging.warning("%s %s " % (m.title, m.published))
    print("-------")
    # квартал года 1 - 4
    for m in Magazine.objects.filter(published__quarter=3, title__isnull=False):
        logging.warning("%s %s " % (m.title, m.published))
    print("////////")
    for b in Bb.objects.filter(rubric__name="Мяу"):
        logging.warning(b.title)
    print("----------")
    for r in Rubric.objects.filter(magazine__price__lte=554):
        logging.warning(r.name)
    print("//////////////")

    f = F("title")
    for b in Bb.objects.filter(title__icontains=f):
        logging.warning(b.title)
    print("---------")
    """    f = F("price")
    for b in Bb.objects.all():
        b.price = f / 2
        b.save()
    for b in Bb.objects.all():
        logging.warning(b.price)"""
    print("/////////////")
    q = Q(rubric__name="Мяу") | Q(rubric__name="Мебель")
    for b in Bb.objects.filter(q):
        logging.warning(b.title)
    print("--------")
    q = Q(rubric__name="Мяу") & ~Q(price__lte=1)
    for b in Bb.objects.filter(q):
        logging.warning(b.title)
    print("///////")
    for b in Bb.objects.order_by("rubric__name", "-price"):
        logging.warning(b)
    print("--------")
    for b in Bb.objects.order_by("rubric__name", "-price").reverse():
        logging.warning(b)
    print("Получение списка полей")
    print([b.name for b in Bb._meta.get_fields()])
    print("//////////")
    print(Bb.objects.aggregate(Min("price")))
    print(Bb.objects.aggregate(max_price=Max("price")))
    print(Bb.objects.aggregate(Min("price"), Max("price")))
    print(Bb.objects.aggregate(diff=Max("price") - Min("price")))
    # также QuerySet поддерживает срезы!
    return HttpResponse(s)


def check_functions_2(request):
    for r in Rubric.objects.annotate(Count("entries")):
        print(r.name, ": ", r.entries__count, sep=" ")
    print("-" * 15)
    for r in Rubric.objects.annotate(cnt=Count("entries")):
        print(r.name, ": ", r.cnt, sep=" ")
    print("-" * 15)
    for r in Rubric.objects.annotate(min_bb=Min("entries")):
        print(r.name, ": ", r.min_bb, sep=" ")
    print("-" * 15)
    for r in Rubric.objects.annotate(
        cnt=Count("entries"), min_bb=Min("entries__price")
    ).filter(cnt__gte=1):
        print(r.name, ": ", r.min_bb, sep=" ")
    print("-------------")
    for r in Rubric.objects.annotate(
        cnt=Count("entries"), filter=Q(entries__price__gt=100)
    ):
        print(r.name, ": ", r.cnt, sep=" ")
    print("-----")
    print(
        Rubric.objects.aggregate(
            sum_r=Sum(
                "entries__price", output_field=IntegerField(), filter=Q(name="Мяу")
            )
        )
    )
    print("---------")
    # Если шо distinct 3.2+ работает в aggregate
    # о чиназес, в классе Q работают модификаторы!
    print(
        Bb.objects.aggregate(
            avg=Avg(("price"), filter=Q(title__iexact="УМПАЛА"), distinct=True)
        )
    )
    # Есть еще StvDev (ср. отклон.) и Variance (дисперсия)
    return HttpResponse("Siiiiuuu!!!")


def calculate_fields(request):
    for b in Bb.objects.annotate(half_price=F("price") / 2):
        print(b.title, b.price, b.half_price)

    for b in Bb.objects.annotate(
        full_name=Concat(F("title"), Value(" ("), F("rubric__name"), Value(")"))
    ):
        print(b.full_name)
    print("-" * 15)
    for b in Bb.objects.annotate(
        half_price=ExpressionWrapper(F("price") / 2, IntegerField())
    ):
        print(b.title, b.half_price)
    print("-" * 15)

    for b in Bb.objects.annotate(
        val=Coalesce("content", "kind", Value("--empty--"), output_field=CharField())
    ):
        print(b.title, ": ", b.val)

    print("-" * 15)
    for b in Bb.objects.annotate(gr=Greatest("price", 500)):
        print(b.title, ": ", b.gr)

    print("-" * 15)
    for b in Bb.objects.annotate(gr=Least("price", 500)):
        print(b.title, ": ", b.gr)

    print("-" * 15)
    for b in Bb.objects.annotate(cast=Cast("price", CharField())):
        print(b.title, ": ", rf"{b.cast}")
    # Также есть Concat, Lower, Upper, Length
    print("--------")
    for b in Bb.objects.annotate(stri=StrIndex("content", Value("лал"))):
        print(b.title, ": ", b.stri)
    return HttpResponse("ANKARA ANKARA ANKARA")
