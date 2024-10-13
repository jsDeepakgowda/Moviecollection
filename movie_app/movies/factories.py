import factory
from django.contrib.auth.models import User
from .models import Collection, Movie

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    user = factory.SubFactory(UserFactory)

class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    genres = factory.Faker('word')
    uuid = factory.Faker('uuid4')
    collection = factory.SubFactory(CollectionFactory)
