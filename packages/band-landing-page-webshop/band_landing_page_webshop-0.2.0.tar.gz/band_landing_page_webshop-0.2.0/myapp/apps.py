"""This file contains app config information"""
from django.apps import AppConfig


class MyappConfig(AppConfig):
    """This class is responsible for configuring the app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
