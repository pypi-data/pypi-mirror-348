import factory

from django.conf import settings
from lotus.factories import CategoryFactory, TagFactory

from ..choices import get_latestflux_template_default
from ..models import ArticleFlux


class ArticleFluxFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of an ``ArticleFlux`` object.
    """
    title = factory.Faker("text", max_nb_chars=20)
    template = get_latestflux_template_default()
    length = 5
    featured_only = False

    class Meta:
        model = ArticleFlux
        skip_postgeneration_save = True

    class Params:
        language = None

    @factory.post_generation
    def from_categories(self, create, extracted, **kwargs):
        """
        Add categories.

        Adopted category language will be either given language code if not empty else
        the default one from settings. This only applies to automically created
        random category, not for the given categories.

        Arguments:
            create (bool): True for create strategy, False for build strategy.
            extracted (object): If ``True``, will create a new random category
                object. If a list assume it's a list of Category objects to add.
                Else if empty don't do anything.
        """
        # Do nothing for build strategy
        if not create or not extracted:
            return

        language = self.language or settings.LANGUAGE_CODE

        # Create a new random category
        if extracted is True:
            categories = [CategoryFactory(language=language)]
        # Take given category objects
        else:
            categories = extracted

        # Add categories
        for category in categories:
            self.from_categories.add(category)

    @factory.post_generation
    def from_tags(self, create, extracted, **kwargs):
        """
        Add tags.

        .. Note::

            This won't works in build strategy since Taggit need to have an object
            primary key to build its generic type relation.

        Arguments:
            create (bool): True for create strategy, False for build strategy.
            extracted (list):  If ``True``, will create a new random tag
                object. If a list assume it's a list of Tag objects to add.
                Else if empty don't do anything.
        """
        if not create or not extracted:
            return

        # Create a new random tag
        if extracted is True:
            tags = [TagFactory()]
        # Take given tag objects
        else:
            tags = extracted

        # Add tags
        self.from_tags.add(*tags)
