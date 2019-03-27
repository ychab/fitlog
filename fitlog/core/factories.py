from django.contrib.auth import get_user_model

import factory
from django.utils.translation import get_language, to_locale

language = get_language() or 'fr-fr'
locale = to_locale(language)

User = get_user_model()


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user_{n}'.format(n=n))
    email = factory.LazyAttribute(lambda o: 'test+{username}@example.com'.format(username=o.username))
    password = factory.PostGenerationMethodCall('set_password', 'test')
    first_name = factory.Faker('first_name', locale=locale)
    last_name = factory.Faker('last_name', locale=locale)

    @classmethod
    def _setup_next_sequence(cls):
        try:
            return User.objects.latest('pk').pk + 1
        except User.DoesNotExist:
            return 1
