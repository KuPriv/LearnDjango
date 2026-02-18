from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

register = template.Library()


@register.filter
def currency(value, name="руб."):
    return "%1.2f %s" % (value, name)


@register.filter(is_safe=True)
def escape_str(value):
    return mark_safe(conditional_escape(value))


@register.simple_tag(takes_context=True)
def lst(context, sep, *args):
    return "%s (итого %s)" % (sep.join(args), len(args))


"""
Use inclusion tags when:
- You have a reusable UI component
- The component has logic + template
- You want DRY (Don’t Repeat Yourself) 
"""
