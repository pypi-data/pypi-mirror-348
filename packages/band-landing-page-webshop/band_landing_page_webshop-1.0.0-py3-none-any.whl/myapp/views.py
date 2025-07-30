# pylint: disable=no-member
"""Views.py - this is where we store This function is useds that render templates"""
from datetime import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import EmailList, ShopItem, Concert, BandMember
from .forms import EmailListForm, InquiryForm
from django.core.mail import send_mail
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt

# HttpResponse

# Create your views here.


def home(request):
    """This function is used to render the home template"""
    band_members = BandMember.objects.all()
    return render(request, "home.html", {"members": band_members})


def shop(request):
    """This function is used to render the shop template with the shop items"""
    shop_items = ShopItem.objects.all()
    return render(request, "shop.html", {"items": shop_items})


def concerts(request):
    """This function is used to render the concerts view"""
    concerts_list = Concert.objects.all()
    return render(request, "concerts.html", {"concerts": concerts_list})


def newsletter(request):
    """This function is used to render the newsletter view"""
    toast_message = None
    toast_type = None

    if request.method == 'POST':
        form = EmailListForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email_address']
            if EmailList.objects.filter(email_address=email).exists():
                toast_message = "This email is already subscribed."
                toast_type = "danger"
            else:
                subscriber = form.save()
                send_mail(
                    subject='Thank you for subscribing!',
                    message=f"Hi {subscriber.first_name}, thanks for joining our newsletter!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email_address],
                    fail_silently=False,
                )
                toast_message = "You've been subscribed to the newsletter!"
                toast_type = "success"
                form = EmailListForm()  # Reset form
        else:
            toast_message = "Please provide both your email and first name."
            toast_type = "danger"
    else:
        form = EmailListForm()

    return render(request, 'news.html', {
        'form': form,
        'toast_message': toast_message,
        'toast_type': toast_type,
    })


def contact(request):
    """This function is used to render the contact view"""
    toast_message = None
    toast_type = None

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # Send email notification
            subject = f"New business inquiry from {inquiry.email_of_sender}"
            message = f"New business inquiry from: {inquiry.email_of_sender}:\n\n{inquiry.content}"
            from_email = settings.DEFAULT_FROM_EMAIL
            # Change this to your email
            recipient_list = [settings.SYSADMIN_DEFAULT_EMAIL_RECIPIENT]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                print("Email sending failed:", e)  # For debugging

            toast_message = "Your message has been sent successfully!"
            toast_type = "success"
            form = InquiryForm()  # reset form
        else:
            toast_message = "Please fill in all fields correctly."
            toast_type = "danger"
    else:
        form = InquiryForm()

    return render(request, 'contact.html', {
        'form': form,
        'toast_message': toast_message,
        'toast_type': toast_type,
    })


def unsubscribe(request, token):
    """This function handles the unsubscription from the newsletter"""
    subscriber = get_object_or_404(EmailList, unsubscribe_token=token)
    if request.method == "POST":
        subscriber.delete()
        messages.success(
            request, "You have been unsubscribed from the mailing list.")
        return redirect("home")  # or a 'goodbye' page

    return render(request, "unsubscribe_confirm.html", {"subscriber": subscriber})


def cart(request):
    """This function handles the shopping cart view"""
    cart_items = request.session.get('cart', None)
    return render(request, "cart.html", {"cart_items": cart_items})


def add_to_cart(request, item_id):
    """This function handles the 'Add to Cart' button in the shop view"""
    quantity = int(request.POST.get('quantity', 1)
                   )  # default to 1 if nothing provided
    cart = request.session.get('cart', [])
    added_item = ShopItem.objects.filter(id=item_id).get()
    for item in cart:
        if item.get("id") == item_id:
            item['quantity'] += quantity
            item['total'] += added_item.price * quantity
            break
    else:
        cart.append({
            'id': added_item.id,
            'title': added_item.title,
            'price': added_item.price,
            'quantity': quantity,
            'total': added_item.price * quantity,
        })

    request.session['cart'] = cart
    return redirect('shop')


def remove_from_cart(request, item_id):
    """This function handles the removal of cart items"""
    cart = request.session.get('cart', [])
    item_id = int(item_id)
    cart = [item for item in cart if item.get('id') != item_id]

    request.session['cart'] = cart
    return redirect('cart')


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def create_checkout_session(request):
    """This function is responsible for creating the Stripe Checkout session"""
    cart = request.session.get('cart', [])
    promo_code = request.POST.get('promo_code')

    if not cart:
        return redirect('cart')

    line_items = []

    for item in cart:
        product = ShopItem.objects.get(id=item['id'])
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(product.price * 100),
                'product_data': {
                    'name': product.title,
                },
            },
            'quantity': item['quantity'],
        })

    session_data = {
        "payment_method_types": ["card"],
        "line_items": line_items,
        "mode": "payment",
        "success_url": request.build_absolute_uri('/checkout/success/'),
        "cancel_url": request.build_absolute_uri('/cart/'),

    }
    if promo_code:
        promotion_code = stripe.PromotionCode.retrieve(promo_code)
        if datetime.fromtimestamp(promotion_code.expires_at) > datetime.now():

            session_data['discounts'] = [{"promotion_code": promo_code}]
    session = stripe.checkout.Session.create(**session_data)

    return redirect(session.url, code=303)


def checkout_success(request):
    """This function handles the successful Stripe Checkout purchase"""
    # Clear the cart
    request.session['cart'] = []
    # Remove the promo code from the session
    if 'promo_code' in request.session:
        del request.session['promo_code']

    return render(request, 'checkout_success.html')


@csrf_exempt
def save_promo_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        promo_code = data.get('promo_code')

        # Save the promo_code to the server-side session
        if promo_code:
            request.session['promo_code'] = promo_code
            return JsonResponse({'status': 'success', 'promo_code': promo_code})
        else:
            return JsonResponse({'status': 'error', 'message': 'Promo code missing'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def promo_expired_while_viewing(request):
    """This function removes the promo code if it expires while the user is viewing the site"""
    if 'promo_code' in request.session:
        del request.session['promo_code']

    return render(request, 'shop.html')
