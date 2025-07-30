from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from ..choices import (
    get_latestflux_template_choices,
    get_latestflux_template_default,
)


class ArticleFlux(CMSPlugin):
    """
    Model for ``ArticleFlux`` plugin parameters.

    Attributes:
        title (models.CharField): An optional title string.
        template (models.CharField): Template choice from available plugin templates
            in setting ``CMSLOTUS_ARTICLE_FLUX_TEMPLATES``. Default to the
            first choice item.
        length (models.PositiveSmallIntegerField): Required positive small integer.
        featured_only (models.BooleanField): Optional boolean.
        from_categories (models.ManyToManyField): Optional choices of Lotus Category
            objects.
        from_tags (models.ManyToManyField): Optional choice of Taggit Tag objects.
    """

    title = models.CharField(
        _("title"),
        max_length=150,
        default="",
    )
    template = models.CharField(
        _("template"),
        blank=False,
        max_length=150,
        choices=get_latestflux_template_choices(),
        default=get_latestflux_template_default(),
    )
    length = models.PositiveSmallIntegerField(
        ("length"),
        default=settings.CMSLOTUS_ARTICLE_FLUX_LIMIT_DEFAULT,
    )
    featured_only = models.BooleanField(
        ("featured only"),
        default=False,
        blank=True,
    )
    from_categories = models.ManyToManyField(
        "lotus.Category",
        verbose_name=_("from categories"),
        related_name="articleflux",
        blank=True,
    )
    from_tags = models.ManyToManyField(
        "taggit.Tag",
        verbose_name=_("from tags"),
        blank=True,
    )

    class Meta:
        verbose_name = _("Article flux")
        verbose_name_plural = _("Article flux")

    def __str__(self):
        return self.title

    def copy_relations(self, oldinstance):
        """
        Copy relations when plugin object is copied as another object.

        See:

        https://docs.django-cms.org/en/latest/how_to/09-custom_plugins.html#handling-relations

        NOTE: Not sure we should use this for categories since they are for specific
        language and plugin can't know about target page language to know if we have
        to adjust or not depending language.
        """
        self.from_tags.set(oldinstance.from_tags.all())
