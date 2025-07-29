# yourapp/admin_views.py
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import NewsletterEmailForm
from .models import EmailList
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import stripe
from datetime import datetime, timedelta


# Make sure you set this properly in your settings.py
stripe.api_key = settings.STRIPE_SECRET_KEY


@staff_member_required
def send_newsletter_view(request):
    toast_message = None
    toast_type = None

    if request.method == "POST":
        form = NewsletterEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            is_cta = form.cleaned_data["is_call_to_action"]
            attach_discount = form.cleaned_data.get("attach_discount", False)
            discount_percentage = form.cleaned_data.get("discount_percentage")
            discount_duration = form.cleaned_data.get("discount_duration")

            coupon_id = None
            if is_cta and attach_discount:
                try:
                    # 1. Create Stripe Coupon
                    coupon = stripe.Coupon.create(
                        percent_off=discount_percentage,
                        duration="once",  # The coupon can be used once per customer
                        name=f"{discount_percentage}% OFF",
                    )

                    current_date = datetime.now()
                    expiration_date = current_date + \
                        timedelta(minutes=discount_duration)
                    # 2. Create a Promotion Code for that Coupon (with expiration if needed)
                    promotion_code = stripe.PromotionCode.create(

                        coupon=coupon.id,
                        expires_at=expiration_date,  # expire after X minutes
                    )

                    coupon_id = promotion_code.id

                except Exception as e:
                    toast_message = f"Failed to create discount: {str(e)}"
                    toast_type = "danger"
                    return render(request, "admin/send_newsletter.html",
                                  {"form": form, 'toast_message': toast_message, 'toast_type': toast_type})

            recipients = EmailList.objects.values()

            for subscriber in recipients:
                email = subscriber.get("email_address")
                name = subscriber.get("first_name")
                unsub_token = subscriber.get("unsubscribe_token")
                unsub_link = f"{settings.DEFAULT_HOST_BASE_URL}/unsubscribe/{unsub_token}"

                # Build the CTA URL
                cta_link = None
                if is_cta:
                    cta_link = f"{settings.DEFAULT_HOST_BASE_URL}/shop/"
                    if coupon_id:
                        cta_link += f"?promo_code={coupon_id}"

                html_message = render_to_string('newsletter-email-template.html',
                                                {'message': message,
                                                 "is_cta": is_cta,
                                                 "cta_link": cta_link,
                                                 "name": name,
                                                 "unsubscribe_link": unsub_link})
                plain_message = strip_tags(html_message)
                send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [
                          email], False, html_message=html_message)

            toast_message = "Letter sent to all subscribers!"
            toast_type = "success"
        else:
            toast_message = "Please fill out the required fields!"
            toast_type = "danger"
    else:
        form = NewsletterEmailForm()

    return render(request, "admin/send_newsletter.html",
                  {"form": form,
                   'toast_message': toast_message,
                   'toast_type': toast_type, })
