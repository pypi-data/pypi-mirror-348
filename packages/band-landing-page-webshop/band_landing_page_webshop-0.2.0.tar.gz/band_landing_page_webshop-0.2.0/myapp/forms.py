"""This file contains the form models"""
from django import forms
from .models import EmailList, Inquiry


class InquiryForm(forms.ModelForm):
    """This class models the 'Contact Us' form"""
    class Meta:
        model = Inquiry
        fields = ['email_of_sender', 'content']
        widgets = {
            'email_of_sender': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': 'required',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message',
                'rows': 4,
                'required': 'required',
            }),
        }

    def clean_email_of_sender(self):
        email = self.cleaned_data.get('email_of_sender')
        if not email:
            raise forms.ValidationError("Email is required.")
        return email

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Message content is required.")
        return content


class EmailListForm(forms.ModelForm):
    """This class models the Newsletter form"""
    class Meta:
        model = EmailList
        fields = ['email_address', 'first_name']
        widgets = {
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address', 'required': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'required': True}),
        }

    def clean_email_address(self):
        email = self.cleaned_data.get('email_address')
        if not email:
            raise forms.ValidationError("Email is required.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("First name is required.")
        return first_name


class NewsletterEmailForm(forms.Form):
    """This form is used on the admin page. The admin can use this form to send a mass email
    to all the people who are subscribed to the email list"""
    subject = forms.CharField(max_length=511)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 10}))
    is_call_to_action = forms.BooleanField(
        required=False, label="Include Call-to-Action Button?")
    attach_discount = forms.BooleanField(required=False)
    discount_percentage = forms.IntegerField(
        required=False, min_value=1, max_value=100, label="Discount percentage (1 - 100)")
    discount_duration = forms.IntegerField(
        # duration in minutes
        required=False, min_value=1, label="Discount duration (minutes)")

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if not subject:
            raise forms.ValidationError("Subject is required.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("Message is required.")
        return message
