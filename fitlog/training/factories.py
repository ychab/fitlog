import factory


class HostFactory(factory.DjangoModelFactory):

    class Meta:
        abstract = True
        django_get_or_create = ('slug',)

    slug = factory.Faker('slug', locale=locale)
    name = factory.LazyAttribute(lambda o: o.slug)
    type = fuzzy.FuzzyChoice(dict(Host.TYPES).keys())
    url = factory.Faker('url', locale=locale)


class OpenGSTHostFactory(HostFactory):

    class Meta:
        model = OpenGSTHost

    version = fuzzy.FuzzyInteger(1, 10)
    platform = fuzzy.FuzzyChoice(dict(OpenGSTHost.PLATFORMS).keys())
