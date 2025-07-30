"""
These are wrappers for field defaults and choices values to be used as a callable.

You should always use these callables to get defaults or choices values instead of
directly use their related settings.

Callables for defaults return a single string. Callables for choices
return a tuple of choice tuples. None of them accept any argument.
"""
from django.conf import settings


def get_latestflux_template_choices():
    return settings.CMSLOTUS_ARTICLE_FLUX_TEMPLATES


def get_latestflux_template_default():
    return settings.CMSLOTUS_ARTICLE_FLUX_TEMPLATES[0][0]
