from datetime import datetime, timezone
from uuid import uuid4

import factory

from src.domain.category.category import Category
from src.domain.genre.genre import Genre


class EntityFactory(factory.Factory):
    id = factory.LazyFunction(uuid4)
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class CategoryFactory(EntityFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class GenreFactory(EntityFactory):
    class Meta:
        model = Genre

    name = factory.Faker("word")
    categories = factory.LazyFunction(lambda: {uuid4()})
