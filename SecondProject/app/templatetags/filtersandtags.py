from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def currency(value, name="руб."):
    return "%1.2f %s" % (value, name)
