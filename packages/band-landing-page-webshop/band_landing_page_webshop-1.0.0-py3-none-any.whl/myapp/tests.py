"""This file contains the unit tests. 50% coverage is required.
Use the 'coverage' python package for verification"""

from .templatetags.discount_tags import discounted_price
from .models import EmailList
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ShopItem
from django.core import mail
from .models import Inquiry

# region template tag tests


class DiscountTemplateTagTest(TestCase):
    """This class is responsible for testing the discount template tag.
    The template tag dynamically calculates the discounted price
    of an item given the original item's price, and a discount percentage"""

    def test_discounted_price_math(self):
        """Testing with whole numbers, works fine"""
        result = discounted_price(100, 20)
        self.assertEqual(result, "80.00")

    def test_discounted_price_wrong_input(self):
        """If the input is interpreted as a string, it should stay untouched"""
        result = discounted_price("14.99", 25)
        self.assertEqual(result, "14.99")

    def test_discounted_price_float(self):
        """Test for rounding errors"""
        result = discounted_price(1299.99, 50)
        self.assertNotEqual(result, 650.00)

    def test_discounted_price_exception(self):
        """Test if TypeError exception is thrown for incorrect price type"""
        self.assertRaises(TypeError, discounted_price, price=None)

# endregion

# region Model tests


class EmailListModelTest(TestCase):
    """This class holds the tests for the creation of an email list subscriber object"""

    def test_email_list_subscriber_creation(self):
        """Test if the email is set correctly"""
        email = EmailList.objects.create(
            email_address="test@example.com", first_name="Test")
        self.assertEqual(email.email_address, "test@example.com")

    def test_first_name_setting(self):
        """Test if the first_name is set correctly"""
        subscriber = EmailList.objects.create(
            email_address="johndoe@asd.com", first_name="Arthur")
        self.assertEqual(subscriber.first_name, "Arthur")

# endregion


# region view tests


class NewsletterAdminViewTest(TestCase):
    """This class is responsible for testing the custom admin page - the newsletter form that
    the admin can use to send an email to every subscriber"""

    def setUp(self):
        """This function performs basic setup, like creating a test client and a test admin user
        and a test subscriber"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password')
        self.subscriber = EmailList.objects.create(
            email_address='subscriber@test.com',
            first_name='Test',
        )

    def test_admin_newsletter_view_get(self):
        """This function tests if the admin can navigate to the page successfully
        The login uses a fake admin account with fake credentials."""
        self.client.login(username='admin', password='password')
        response = self.client.get('/send-newsletter/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/send_newsletter.html')

    def test_post_send_newsletter_invalid_form(self):
        """This function tests if the admin submits and empty form, the errors are handled properly
        and the admin is prompted to fill out the required fields. The login uses
        a fake admin account with fake credentials."""
        self.client.login(username='admin', password='password')
        response = self.client.post(
            '/send-newsletter/', data={})  # empty form data
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please fill out the required fields")

    def test_post_newsletter_without_cta_or_discount(self):
        """This function tests if the email is actually sent. Specifically,
        this function tests an email that doesn't have a call-to-action button
        The login uses a fake admin account with fake credentials."""
        data = {
            "subject": "Hello!",
            "message": "Test email body.",
            "is_call_to_action": False,  # No CTA
        }
        self.client.login(username='admin', password='password')
        response = self.client.post('/send-newsletter/', data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Letter sent to all subscribers")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Hello', mail.outbox[0].subject)


class ShopViewTests(TestCase):
    """This class handles the test cases for the shop view"""

    def setUp(self):
        """Basic setup, create a test client and some shop items"""
        self.client = Client()
        ShopItem.objects.create(title="Test Item", price=100.0, available=True)

    def test_shop_view_renders_correctly(self):
        """This function verifies that the user can navigate to the shop and see the items"""
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
        self.assertContains(response, "Test Item")


class CheckoutSuccessTests(TestCase):
    """This class is responsible for testing the custom checkout success page"""

    def setUp(self):
        """Perform basic setup, like creating a test client, session, and shopping cart items"""
        self.client = Client()
        session = self.client.session
        session['cart'] = [{'item_id': 1, 'quantity': 2}]
        session.save()

    def test_checkout_success_clears_cart(self):
        """This function tests that if the user is sent to the checkout_success.html page,
        then the page is sent properly (response status 200) and the cart becomes empty
        in the session storage"""
        response = self.client.get(reverse('checkout_success'))
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertEqual(session.get('cart'), [])
        self.assertTemplateUsed(response, 'checkout_success.html')


class CartViewTests(TestCase):
    """This class handles test cases for the cart view"""

    def setUp(self):
        """Basic setup, create a test client"""
        self.client = Client()

    def test_cart_view_works(self):
        """This function verifies that the cart view can be seen, and cart data loads properly"""
        session = self.client.session
        session['cart_items'] = [{'item_id': 1, 'quantity': 1}]
        session.save()
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        # adjust name if different
        self.assertTemplateUsed(response, 'cart.html')


class ContactViewTests(TestCase):
    """This class handles the contact form view test cases"""

    def setUp(self):
        """Basic setup, create a test client"""
        self.client = Client()

    def test_contact_view_get(self):
        """This function tests if the page itself can be seen by users"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIn('form', response.context)

    def test_contact_view_post_valid_data(self):
        """This function tests if the form works with valid data"""
        data = {
            'email_of_sender': 'test@example.com',
            'content': 'This is a test message'
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Your message has been sent successfully!')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'New business inquiry from test@example.com')
        self.assertTrue(Inquiry.objects.filter(
            email_of_sender='test@example.com').exists())

    def test_contact_view_post_invalid_data(self):
        """This function tests if the form works with invalid data"""

        data = {
            'email_of_sender': '',  # Invalid: empty email
            'content': ''
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please fill in all fields correctly.')
        self.assertEqual(len(mail.outbox), 0)


class NewsletterViewTests(TestCase):
    """This class handles the newsletter subscription form test cases"""

    def setUp(self):
        """Basic setup, create a test client"""
        self.client = Client()

    def test_newsletter_view_get(self):
        """This function tests if the template can be accessed by users"""
        response = self.client.get(reverse('newsletter'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news.html')
        self.assertIn('form', response.context)

    def test_newsletter_post_valid_new_email(self):
        """This function tests if the form works with valid input"""
        data = {
            'email_address': 'newuser@example.com',
            'first_name': 'Alice'
        }
        response = self.client.post(reverse('newsletter'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "subscribed to the newsletter!")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('thank you', mail.outbox[0].subject.lower())
        self.assertTrue(EmailList.objects.filter(
            email_address='newuser@example.com').exists())

    def test_newsletter_post_duplicate_email(self):
        """This function tests if users are prevented from subscribing twice with the same email address"""
        EmailList.objects.create(
            email_address='already@there.com', first_name='Bob')
        data = {
            'email_address': 'already@there.com',
            'first_name': 'Bob'
        }
        response = self.client.post(reverse('newsletter'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This email is already subscribed.")
        self.assertEqual(len(mail.outbox), 0)

    def test_newsletter_post_invalid_data(self):
        """This function tests if the form handles invalid data properly"""
        data = {
            'email_address': '',  # Invalid
            'first_name': ''
        }
        response = self.client.post(reverse('newsletter'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Please provide both your email and first name.")
        self.assertEqual(len(mail.outbox), 0)

# endregion
