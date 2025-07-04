from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

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
    print(m1.spares.all())
    s1.machine_set.all()
    m1.spares.add(s3)
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
