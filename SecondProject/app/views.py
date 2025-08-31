import logging
import os
from datetime import datetime, timezone, timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.paginator import Paginator
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
    Case,
    When,
    Subquery,
    OuterRef,
    Exists,
    Prefetch,
)
from django.forms import (
    modelform_factory,
    DecimalField,
    Select,
    modelformset_factory,
    BaseModelFormSet,
    inlineformset_factory,
)
from django.forms.formsets import ORDERING_FIELD_NAME
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotFound,
    StreamingHttpResponse,
    FileResponse,
    HttpResponseForbidden,
)
from django.db.models.functions import (
    Concat,
    Coalesce,
    Greatest,
    Least,
    Cast,
    StrIndex,
    Now,
    Extract,
)
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse, reverse_lazy, resolve
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    ListView,
    CreateView,
    TemplateView,
    DetailView,
    FormView,
    UpdateView,
    DeleteView,
    ArchiveIndexView,
    DateDetailView,
    RedirectView,
)
from django.views.generic.detail import SingleObjectMixin

from .forms import BbForm, RegisterUserForm
from .models import *


def index(request):
    """success_url = reverse_lazy("index")
    resp_content = ("Здесь ", "будет ", "главная ", "страница ", "сайта!")
    resp = StreamingHttpResponse(resp_content, content_type="text/html; charset=utf-8")
    return resp"""
    print(request.user.is_authenticated)
    print(request.user.has_perm("app:add_rubric"))
    print(
        request.user.has_perms(
            ("app:add_rubric", "app:change_rubric", "app:delete_rubric")
        )
    )
    print(request.user.username)
    # print(User.objects.with_perm("app.add_bb"))

    print(request.user.get_user_permissions())
    print(request.user.get_group_permissions())
    print(request.user.get_all_permissions())
    bbs = Bb.objects.all().order_by("price")
    rubrics = Rubric.objects.all()
    paginator = Paginator(bbs, 2)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)
    context = {"bbs": bbs, "page": page, "rubrics": rubrics}
    return render(request, "app/index.html", context)


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

    for b in Bb.objects.annotate(n=Now()):
        print(b.title, ": ", b.n)

    for m in Magazine.objects.annotate(ex=Extract("published", "year")):
        print(m.title, ": ", m.ex)

    # И еще куча разных методов однотипных (стр 159+)

    for r in Rubric.objects.annotate(
        cnt=Count("entries"),
        cnt_s=Case(
            When(cnt__gte=5, then=Value("Много")),
            When(cnt__gte=3, then=Value("Средне")),
            When(cnt__gte=1, then=Value("Мало")),
            default=Value("Вообще нет"),
            output_field=CharField(),
        ),
    ):
        print(r.name, ": ", r.cnt, ": ", r.cnt_s)

    sq = Subquery(
        Magazine.objects.filter(rubric=OuterRef("pk"))
        .order_by("-published")
        .values("published")[:1]
    )
    for r in Rubric.objects.annotate(last_bb_date=sq):
        print(r.name, ": ", r.last_bb_date)

    subq = Exists(Magazine.objects.filter(rubric=OuterRef("pk"), price__gt=333))
    for r in Rubric.objects.annotate(is_expensive=subq).filter(is_expensive=True):
        print(r.name)

    m1 = Magazine.objects.filter(price__gte=333).order_by()
    m2 = Magazine.objects.filter(rubric__name="Мяу").order_by()
    for m in m1.union(m2):
        print(m.title, ": ", m.price)
    # также difference и intersection

    print(Bb.objects.values("title", "price", "rubric"))
    # при вызове values без параметров будет выдан также QuerySet, но вместо имен полей модели
    # будут поля из БД

    print(Bb.objects.values_list())

    print(Magazine.objects.dates("published", "day"))
    print(Magazine.objects.dates("published", "month"))
    print(Magazine.objects.datetimes("published", "month"))

    return HttpResponse("ANKARA ANKARA ANKARA")


class WriteSomeFunctions(View):

    @staticmethod
    def first_function(self, request):
        ...
        return HttpResponse("Hi!")


class RubricListView(ListView):
    model = Rubric
    template_name = "index.html"
    context_object_name = "rubrics"


def by_rubric(request, rubric_id):
    print(
        request.method,
        request.scheme,
        request.META,
        request.encoding,
    )
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {"bbs": bbs, "rubrics": rubrics, "current_rubric": current_rubric}
    return render(request, "app/by_rubric.html", context)


def add_bb_and_save(request):
    if request.method == "POST":
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(
                reverse(
                    "app:by_rubric", kwargs={"rubric_id": bbf.cleaned_data["rubric"].pk}
                )
            )
        else:
            context = {"form": bbf}
            return render(request, "app/create.html", context)
    else:
        bbf = BbForm()
        context = {"form": bbf}
        return render(request, "app/create.html", context)


def detailw(request, bb_id):
    try:
        bb = Bb.objects.get(pk=bb_id)
    except Bb.DoesNotExist:
        return HttpResponseNotFound("Не существует.")
        # HttpResponseForbidden, BadRequest, NotModifed, Done, e.t.c.
    return HttpResponse(...)


def detail2(request, rubric_id):
    bb = get_object_or_404(Bb, rubric=rubric_id)
    bbs = get_list_or_404(Bb, rubric=rubric_id)
    print(bb)
    print(bbs)
    return HttpResponse(...)


def send_file(request):
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent
    cat_path = BASE_DIR / "media/cat.jfif"
    return FileResponse(open(cat_path, "rb"))
    # as_attachment=True - скачивает файл


def check_resolve(request):
    r = resolve("/app/rubric/7")
    print(r.kwargs)
    print(r.url_name)
    print(r.view_name)
    print(r.route)
    print(r.app_name)
    print(r.namespace)
    return HttpResponse(...)


@require_http_methods(["GET", "POST"])
def add(request): ...


class BbCreateView(LoginRequiredMixin, CreateView):
    template_name = "app/create.html"
    model = Bb
    fields = ["title", "price", "rubric"]
    success_url = reverse_lazy("app:by_rubric")


class BbByRubricView(TemplateView):
    template_name = "app/by_rubric.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bbs"] = Bb.objects.filter(rubric=context["rubric_id"])
        context["rubrics"] = Rubric.objects.all()
        context["current_rubric"] = Rubric.objects.get(pk=context["rubric_id"])
        return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context


class BbByRubricViewList(ListView):
    template_name = "app/by_rubric.html"
    context_object_name = "bbs"

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs["rubric_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rubrics"] = Rubric.objects.all()
        context["current_rubric"] = Rubric.objects.get(pk=self.kwargs["rubric_id"])

        return context


class BbAddView(FormView):
    template_name = "app/create.html"
    form_class = BbForm
    initial = {"price": 0.0}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse(
            "app:by_rubric", kwargs={"rubric_id": self.object.cleaned_data["rubric"].pk}
        )


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = "/app"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = "/app"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = "created_at"
    date_list_period = "day"
    template_name = "app/archive_index.html"
    context_object_name = "bbs"
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context["object_list"])
        print(context["date_list"])
        context["rubric"] = Rubric.objects.all()
        return context


class BbDateDetailView(DateDetailView):
    model = Bb
    date_field = "created_at"
    month_format = "%m"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rubrics"] = Rubric.objects.all()
        return context


class BbRedirectView(RedirectView):
    url = "/app/detail/%(pk)d"
    permanent = True


class BbByRubricMixinView(SingleObjectMixin, ListView):
    template_name = "app/by_rubric.html"
    pk_url_kwarg = "rubric_id"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_rubric"] = self.object
        context["rubric"] = Rubric.objects.all()
        context["bbs"] = context["object_list"]
        return context

    def get_queryset(self):
        return self.object.entries.all()


class BbCreateFormView(CreateView):
    BbForm = modelform_factory(
        Bb,
        fields=("title", "content", "price", "rubric"),
        labels={"title": "Название товара"},
        help_texts={"rubric": "Не забудь выбрать рубрику"},
        field_classes={"price": DecimalField},
        widgets={"rubric": Select(attrs={"size": 8})},
    )

    form_class = BbForm
    template_name = "app/create.html"
    success_url = reverse_lazy("app:index")


class RegisterUserFormView(CreateView):
    model = User
    form_class = RegisterUserForm
    # form_class = UserCreationForm
    template_name = "app/register.html"
    success_url = reverse_lazy("app:index")


def edit(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == "POST":
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(
                reverse(
                    "app:by_rubric", kwargs={"rubric_id": bbf.cleaned_data["rubric"].pk}
                ),
            )
    else:
        bbf = BbForm(instance=bb)

    context = {"form": bbf}
    return render(request, "app/bb_form.html", context)


@permission_required(
    ("app.add_rubric", "app.delete_rubric", "app.change_rubric"),
    login_url=reverse_lazy("accounts:login"),
)
def rubrics(request):
    # Если это CBV используем AccessMixin
    # Также есть LoginRequiredMixin, UserPassesTestMixin
    # (test_func переопределить), PermissionRequiredMixin
    RubricFormSet = modelformset_factory(
        Rubric,
        fields=("name",),
        can_order=True,
        can_delete=True,
        formset=RubricBaseFormSet,
    )
    formset = RubricFormSet(request.POST or None)

    if request.method == "POST" and formset.is_valid():
        for form in formset:
            if form.cleaned_data:
                rubric = form.save(commit=False)
                rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
                rubric.save()
        return redirect("app:index")

    return render(request, "app/rubric_formset.html", {"formset": formset})


class RubricBaseFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        names = [
            form.cleaned_data["name"]
            for form in self.forms
            if "name" in form.cleaned_data
        ]
        if ("Мяу" not in names) or ("Мяучик" not in names):
            raise ValidationError("РУБРИК С МЯУКАЛКАМИ НЕ ХВАТАЕТ")


def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == "POST":
        formset = BbsFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            formset.save()
            return redirect("app:index")
    else:
        formset = BbsFormSet(instance=rubric)
    context = {"formset": formset, "current_rubric": rubric}
    return render(request, "app/bbs.html", context)


def test_select_prefetch_related(request):
    b = get_object_or_404(Bb, pk=40)
    print(b.rubric.name)
    b2 = Bb.objects.select_related("rubric").get(pk=40)
    print(b2.rubric.name)
    b3 = Bb.objects.select_related("rubric__super_rubric").get(pk=70)
    print(b3.rubric.super_rubric.title)
    b4 = Bb.objects.select_related("rubric", "rubric__super_rubric").get(pk=70)
    print(b4.rubric.super_rubric.title)
    r = Rubric.objects.prefetch_related("entries").first()
    for bb in r.entries.all():
        print(bb.title)
    m = Machine.objects.prefetch_related("spares").first()
    for s in m.spares.all():
        print(s.name)

    print("Класс Prefetch ///")
    pr1 = Prefetch("entries", queryset=Bb.objects.order_by("title"))
    r = Rubric.objects.prefetch_related(pr1).first()
    for bb in r.entries.all():
        print(bb.title)

    print("pr 2 //// ")
    pr2 = Prefetch(
        "entries", queryset=Bb.objects.filter(price__lt=1000), to_attr="expensive"
    )
    r = Rubric.objects.prefetch_related(pr2).get(pk=10)
    for bb in r.expensive:
        print(bb.title)

    bb = Bb.objects.defer("content").get(pk=41)
    print(bb.title)
    print(bb.content)

    bb = Bb.objects.only("title", "price").get(pk=41)
    # defer - отдельные запросы в будущем для заданных полей
    # only - извлекает только эти поля запросами, можно вызвать defer потом, но вызов only сбрасывает
    # only и defer, определенные до этого
    return HttpResponse(" ")
