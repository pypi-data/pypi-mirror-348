"""
Compatibility module for Django version differences.
"""
import django

# JSONField location changed in Django 3.1
if django.VERSION >= (3, 1):
    from django.db.models import JSONField
else:
    from django.contrib.postgres.fields import JSONField
