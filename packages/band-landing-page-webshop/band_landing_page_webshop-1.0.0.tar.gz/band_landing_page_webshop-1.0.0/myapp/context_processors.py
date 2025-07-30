"""This file handles the globally available context variables (global app state)"""
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def cart_count(request):
    """This function handles the cart count so we can show a small widget on top of the cart icon"""
    cart = request.session.get('cart', [])
    total_items = sum(item.get('quantity', 1) for item in cart)
    return {
        'cart_count': total_items
    }


def promo_code_context(request):
    """This function handles the promo code decoding to apply UI changes"""
    promo_code = request.session.get('promo_code')
    promo_data = None

    if promo_code:
        try:
            promotion_code = stripe.PromotionCode.retrieve(promo_code)

            if promotion_code.active and promotion_code.coupon.valid:
                promo_data = {
                    'discount_percent': promotion_code.coupon.percent_off,
                    'expires_at': promotion_code.expires_at,  # can be None
                    'promo_code': promo_code
                }
        except Exception as e:
            print(f"Error fetching promotion code: {e}")
            # Optionally clear bad promo codes from session
            del request.session['promo_code']

    return {
        'promo_data': promo_data
    }
