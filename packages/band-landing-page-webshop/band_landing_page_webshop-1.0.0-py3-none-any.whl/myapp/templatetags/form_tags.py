"""In this file, we create a custom template tag (filter, or pipe) that handles class handling"""
from django import template
from django.forms.boundfield import BoundField

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={'class': css_class})
    return field  # fallback, just return it as-is
