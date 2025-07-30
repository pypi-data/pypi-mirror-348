from django.conf import settings
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from lotus.models import Article
from lotus.views.mixins import ArticleFilterAbstractView

from ..choices import get_latestflux_template_default
from ..forms import ArticleFluxForm
from ..models import ArticleFlux


class ArticleFluxPlugin(CMSPluginBase):
    """
    DjangoCMS plugin publisher for ``ArticleFlux``.
    """
    module = _("Lotus")
    name = _("Article flux")
    model = ArticleFlux
    form = ArticleFluxForm
    render_template = get_latestflux_template_default()
    cache = False

    class Media:
        css = settings.CMSLOTUS_ADMIN_ARTICLE_FLUX_ASSETS.get("css", None)
        js = settings.CMSLOTUS_ADMIN_ARTICLE_FLUX_ASSETS.get("js", None)

    def get_fieldsets(self, request, obj=None):
        """
        Define plugin form fieldsets.

        .. todo::
            Template may be hidden when there is only a single choice since it will
            be forced as default.
        """
        fieldsets = [
            (None, {
                "fields": (
                    "title",
                ),
            }),
            (_("Options"), {
                "fields": (
                    "featured_only",
                    ("template", "length"),
                    "from_categories",
                    "from_tags",
                ),
            }),
        ]

        return tuple(fieldsets)

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        self.render_template = instance.template

        from_categories = instance.from_categories.all()
        from_tags = instance.from_tags.all()

        queryset_filter = ArticleFilterAbstractView()
        queryset_filter.request = context["request"]

        articles = queryset_filter.apply_article_lookups(
            Article.objects,
            context["lang"]
        )

        if instance.featured_only is True:
            articles = articles.exclude(featured=False)

        if from_categories:
            articles = articles.filter(categories__in=from_categories)

        if from_tags:
            articles = articles.filter(tags__in=from_tags)

        articles = articles.order_by(*Article.COMMON_ORDER_BY)

        # Distinct object list to avoid twices from queryset lookups
        articles = articles.distinct()

        # Finally apply possible slicing for defined length
        if instance.length:
            articles = articles[0:instance.length]

        context.update({
            "instance": instance,
            "articles": articles,
            "from_tags": from_tags,
            "from_categories": from_categories,
        })

        return context
