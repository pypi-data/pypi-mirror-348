from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from lotus.formfields import TranslatedModelMultipleChoiceField
from lotus.models import Category
from taggit.models import Tag

from ..models.article import ArticleFlux


class ArticleFluxForm(forms.ModelForm):
    """
    Form controller for plugin ``ArticleFlux``.
    """
    class Meta:
        model = ArticleFlux
        exclude = []
        fields = [
            "title",
            "template",
            "length",
            "featured_only",
            "from_categories",
            "from_tags",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category_queryset = Category.objects.all().order_by(*Category.COMMON_ORDER_BY)

        tag_queryset = Tag.objects.all().order_by("name")

        self.fields["from_categories"] = TranslatedModelMultipleChoiceField(
            queryset=category_queryset,
            widget=FilteredSelectMultiple("categories", is_stacked=False),
            required=False,
            blank=True,
        )

        self.fields["from_tags"] = forms.ModelMultipleChoiceField(
            queryset=tag_queryset,
            widget=FilteredSelectMultiple("tags", is_stacked=False),
            required=False,
            blank=True,
        )
