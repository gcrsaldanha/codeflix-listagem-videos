from datetime import datetime, timezone
from uuid import uuid4

import factory

from src.domain.category.category import Category


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    id = factory.LazyFunction(uuid4)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    is_active = factory.Faker("boolean")
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
