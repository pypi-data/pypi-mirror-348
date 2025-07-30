"""
The `compatibility` module provides support for backwards compatibility with older
versions of Django/Python, and compatibility wrappers around optional packages.
"""
# allow JSONFIELD for django to be from either django fields or postgres fields
try:
    from django.db.models.JSONField import JSONField, ArrayField
except ImportError:
    from django.contrib.postgres.fields import JSONField, ArrayField

