"""This file is responsible for comfortable user interaction upon installation"""
import os
import sys
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")


def main():
    execute_from_command_line(sys.argv)
