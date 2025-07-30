"""This file is where we define the routing inside my app"""
from django.urls import path
from . import views
from . import admin_views
urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("contact/", views.contact, name="contact"),
    path("news/", views.newsletter, name="newsletter"),
    path("concerts/", views.concerts, name="concerts"),
    path("unsubscribe/<uuid:token>/", views.unsubscribe, name="unsubscribe"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:item_id>/",
         views.remove_from_cart, name="remove_from_cart"),
    path('save-promo-code/', views.save_promo_code, name='save_promo_code'),
    path("promo-expired-while-viewing/", views.promo_expired_while_viewing,
         name="promo_expired_while_viewing"),
    # stripe views
    path("create-checkout-session/", views.create_checkout_session,
         name="create_checkout_session"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),

    # admin views
    path("send-newsletter/", admin_views.send_newsletter_view,
         name="send_newsletter"),


]
