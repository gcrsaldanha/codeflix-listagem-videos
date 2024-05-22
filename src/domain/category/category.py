from dataclasses import dataclass

from src.domain.entity import Entity


@dataclass(eq=False)
class Category(Entity):
    name: str
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            self.notification.add_error("name cannot be longer than 255")

        if not self.name:
            self.notification.add_error("name cannot be empty")

        if len(self.description) > 1024:
            self.notification.add_error("description cannot be longer than 1024")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def __str__(self):
        return f"{self.name} - {self.description} ({self.is_active})"

    def __repr__(self):
        return f"<Category {self.name} ({self.id})>"
