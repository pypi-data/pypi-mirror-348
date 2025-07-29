from enum import Enum
from typing import Optional, Dict, Any, List, Set

from pydantic import Field

from .base import NocodbModel, AttachmentObject
from .types import LongText


class Currency(str, Enum):
    USD = "USD"
    RUB = "RUB"
    CZK = "CZK"
    UAH = "UAH"
    GBP = "GBP"
    EUR = "EUR"

class CheckoutMode(Enum):
    BOOKING = "BOOKING"
    PAYMENT = "PAYMENT"

class ShopCategory(NocodbModel):
    __external_id_field__ = "External ID"
    __skip_update_attributes__ = [] # ["image"]
    __default_lang__ = "EN"

    # Define field mappings once at class level
    __field_mappings__ = {
        "name": {"RU": "Название", "EN": "Name"},
        "image": {"RU": "Изображение", "EN": "Image"},
        "external_id": {"RU": "External ID", "EN": "External ID"}
        # "parent_categories": {"RU": "Назначить родительскую категорию", "EN": "Set parent category"}
    }

    id: str
    name: str
    image: Optional[AttachmentObject] = None

    def __init__(self, *args, lang: Optional[str] = None, **data):
        super().__init__(*args, **data)
        # stash the mapped data for later:
        self.nocodb_data = self.to_nocodb(lang)

    @classmethod
    def __nocodb_field_name__(cls, field_key: str, lang: Optional[str] = None) -> str:
        """Get localized NocoDB field name for a given field key

        Args:
            field_key: Key of the field in __field_mappings__
            lang: Language code (EN or RU), defaults to client's language

        Returns:
            Localized field name
        """
        lang = lang or cls.__default_lang__
        return cls.__field_mappings__[field_key][lang]

    def __nocodb_table_schema__(self, lang: Optional[str] = None) -> dict:
        """Get expected NocoDB table schema to ensure type consistency

        Args:
            lang: Language code (EN or RU), defaults to client's language

        Returns:
            Dictionary mapping field names to their expected NocoDB types
        """
        lang = lang or self.__default_lang__
        return {
            self.__nocodb_field_name__("name", lang): str,
            self.__nocodb_field_name__("image", lang): AttachmentObject,
            self.__nocodb_field_name__("external_id", lang): str
        }

    def __skip_update_column_names__(self, lang: Optional[str] = None) -> list[str]:
        column_names: list[str] = []
        if not self.__skip_update_attributes__:
            return column_names
        lang = lang or self.__default_lang__
        for attribute in self.__skip_update_attributes__:
            column_names.append(self.__nocodb_field_name__(attribute, lang))
        return column_names

    def __mapper__(self, lang: Optional[str] = None) -> dict:
        """Map instance data to NocoDB format

        Args:
            lang: Language code (EN or RU), defaults to client's language

        Returns:
            Dictionary with mapped data in NocoDB format
        """
        lang = lang or self.__default_lang__
        mapped_data: Dict[str, Any] = {
            "id": self.id,
            self.__nocodb_field_name__("name", lang): self.name,
            self.__nocodb_field_name__("external_id", lang): self.id
        }

        # Format image data for NocoDB
        if self.image:
            image_field = self.__nocodb_field_name__("image", lang)
            mapped_data[image_field] = [
                {
                    "url": str(self.image.url),
                    "title": f"image-{self.id}.jpg",
                    "mimetype": "image/jpeg"
                }
            ]
        if self.__skip_update_attributes__:
            for skip_attr in self.__skip_update_attributes__:
                mapped_data.pop(self.__nocodb_field_name__(skip_attr, lang), None)

        return mapped_data
    
        # ergonomic alias
    def to_nocodb(self, lang: Optional[str] = None) -> Dict[str, Any]:
        return self.__mapper__(lang)


class ShopProduct(NocodbModel):
    __external_id_field__ = "External ID"
    __skip_update_attributes__ = []  # [e.g: "image"]
    __default_lang__ = "EN"

    # Define field mappings once at class level
    __field_mappings__ = {
        "name": {"RU": "Название", "EN": "Name"},
        "description": {"RU": "Описание", "EN": "Description"},
        "images": {"RU": "Изображения", "EN": "Images"},
        "price": {"RU": "Стоимость", "EN": "Price"},
        "final_price": {"RU": "Стоимость со скидкой", "EN": "Discounted price"},
        "currency": {"RU": "Валюта", "EN": "Currency"},
        "stock_qty": {"RU": "Доступное количество", "EN": "Available quantity"},
        "external_id": {"RU": "Внешний ID", "EN": "External ID"},
        "checkout_mode": {"RU": "Режим оплаты", "EN": "Checkout mode"},
        "category": {"RU": "Категория", "EN": "Category"},
        "parent_categories": {"RU": "Назначить родительскую категорию", "EN": "Set parent category"}
    }

    id: str
    name: str
    price: float
    description: Optional[str] = None
    final_price: Optional[float] = None
    currency: Optional[Currency] = None
    stock_qty: Optional[int] = None
    images: Optional[List[AttachmentObject]] = Field(
        default=None,
        description="Shop product images",
        json_schema_extra={"nocodb_type": "Attachment"}
    )
    checkout_mode: Optional[List[str]] = None
    extra_attributes: Optional[List[Dict[str, str]]] = None
    categories: Optional[List['ShopCategory']] = []

    def __init__(self, *args, lang: Optional[str] = None, **data):
        super().__init__(*args, **data)
        # stash the mapped data for later:
        self.nocodb_data = self.to_nocodb(lang)

    @classmethod
    def __nocodb_field_name__(cls, field_key: str, lang: Optional[str] = None) -> str:
        """Get localized NocoDB field name for a given field key
        Args:
            field_key: Key of the field in __field_mappings__
            lang: Language code (EN or RU), defaults to client's language

        Returns:
            Localized field name
        """

        lang = lang or cls.__default_lang__
        return cls.__field_mappings__[field_key][lang]

    def __nocodb_table_schema__(self, lang: Optional[str] = None) -> dict:
        """Get expected NocoDB table schema to ensure type consistency

        Args:
            lang: Language code (EN or RU), defaults to client's language

        Returns:
            Dictionary mapping field names to their expected NocoDB types
        """

        lang = lang or self.__class__.__default_lang__
        schema = {
            self.__nocodb_field_name__("name", lang): str,
            self.__nocodb_field_name__("description", lang): LongText,
            self.__nocodb_field_name__("images", lang): AttachmentObject,
            self.__nocodb_field_name__("price", lang): float,
            self.__nocodb_field_name__("final_price", lang): float,
            self.__nocodb_field_name__("currency", lang): Currency,
            self.__nocodb_field_name__("stock_qty", lang): int,
            self.__nocodb_field_name__("external_id", lang): str,
            self.__nocodb_field_name__("checkout_mode", lang): List[str],
        }
        if self.extra_attributes:
            for attr in self.extra_attributes:
                if name := attr.get("name"):
                    schema[name] = str
        return schema

    def __mapper__(self, lang: Optional[str] = None) -> dict:
        """Map instance data to NocoDB format

        Args:
            lang: Language code (EN or RU), defaults to client's language

        Returns:
            Dictionary with mapped data in NocoDB format
        """
        lang = lang or self.__class__.__default_lang__
        mapped_data = {
            "id": self.id,
            self.__nocodb_field_name__("name", lang): self.name,
            self.__nocodb_field_name__("external_id", lang): self.id,
            self.__nocodb_field_name__("price", lang): self.price,
        }
        if self.description:
            mapped_data[self.__nocodb_field_name__("description", lang)] = self.description
        if self.final_price is not None:
            mapped_data[self.__nocodb_field_name__("final_price", lang)] = self.final_price
        if self.currency:
            mapped_data[self.__nocodb_field_name__("currency", lang)] = self.currency
        if self.stock_qty is not None:
            mapped_data[self.__nocodb_field_name__("stock_qty", lang)] = self.stock_qty
        # Format images for NocoDB
        if self.images:
            images = []
            for i, attachment in enumerate(self.images):
                images.append({
                    "url": attachment.url,
                    "title": f"image-{self.id}-{i}.jpg",
                    "mimetype": "image/jpeg"
                })
            mapped_data[self.__nocodb_field_name__("images", lang)] = images

        # Add extra attributes
        if self.extra_attributes:
            for attr in self.extra_attributes:
                if attr.get("name") and attr.get("description"):
                    mapped_data[attr["name"]] = attr["description"]

        if self.__skip_update_attributes__:
            for skip_attr in self.__skip_update_attributes__:
                mapped_data.pop(self.__nocodb_field_name__(skip_attr, lang), None)

        return mapped_data

    # ergonomic alias
    def to_nocodb(self, lang: Optional[str] = None) -> Dict[str, Any]:
        return self.__mapper__(lang)