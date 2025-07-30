"""In this file, we create a custom template tag which handles the UI change if there is a discount"""
from django import template

register = template.Library()


@register.filter
def discounted_price(price, discount_percent):
    try:
        discounted = price * (1.0 - (discount_percent / 100))
        return f"{discounted:.2f}"
    except (TypeError, ValueError):
        return price
