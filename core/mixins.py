from typing import Type, Any


class ORMConvertibleMixin:
    @classmethod
    def to_orm(cls, orm_class: Type[Any], instance: Any) -> Any:

        data = {}
        for field in vars(instance):
            # ігноруємо приватні поля або інші internal атрибути
            if not field.startswith("_"):
                data[field] = getattr(instance, field)
        return orm_class(**data)
