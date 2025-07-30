"""In this file, we register our models for the admin page"""
from django.contrib import admin
from .models import ShopItem, EmailList, BandMember, Concert, Inquiry


# Register your models here.
admin.site.register(ShopItem)
admin.site.register(EmailList)
admin.site.register(BandMember)
admin.site.register(Concert)
admin.site.register(Inquiry)
