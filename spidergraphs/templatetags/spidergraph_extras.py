from django import template

register = template.Library()

@register.filter
def percentage(decimal):
    if decimal is not None:
        return str(round(decimal * 100,1)) + "%"
    return ""

