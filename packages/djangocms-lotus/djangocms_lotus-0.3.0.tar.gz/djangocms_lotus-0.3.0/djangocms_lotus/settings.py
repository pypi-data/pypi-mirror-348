"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

"""
CMSLOTUS_ARTICLE_FLUX_TEMPLATES = (
    ("djangocms_lotus/article-flux/default.html", "Default"),
)
"""
List of template choices available to render Article flux plugin.
"""

CMSLOTUS_ARTICLE_FLUX_LIMIT_DEFAULT = 5
"""
Default limit of articles to display in Article flux plugin.
"""

CMSLOTUS_ADMIN_ARTICLE_FLUX_ASSETS = {
    "css": {
        "all": ("css/cmslotus-admin/article-flux.css",)
    },
    "js": None,
}
"""
Form medias to load in all ArticleFlux plugin form that may allow you to adjust plugin
form layout. See Django documentation about
`admin form media definitions <https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-asset-definitions>`_
to know how you can edit it.
"""  # noqa
