"""Domain models for the tiny shop benchmark."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Iterable


class CustomerTier(str, Enum):
    STANDARD = "standard"
    SILVER = "silver"
    GOLD = "gold"
    STAFF = "staff"


class OrderStatus(str, Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class Customer:
    id: str
    email: str
    tier: CustomerTier = CustomerTier.STANDARD
    store_credit_cents: int = 0
    country: str = "US"

    def has_credit(self) -> bool:
        return self.store_credit_cents > 0

    def can_receive_promos(self) -> bool:
        return "@" in self.email and not self.email.endswith("@example.invalid")


@dataclass(slots=True)
class Product:
    sku: str
    name: str
    price_cents: int
    category: str
    taxable: bool = True
    fragile: bool = False
    discontinued: bool = False

    def is_available(self) -> bool:
        return not self.discontinued and self.price_cents > 0


@dataclass(slots=True)
class LineItem:
    product: Product
    quantity: int
    gift_wrap: bool = False

    def subtotal_cents(self) -> int:
        return self.product.price_cents * self.quantity

    def requires_special_packaging(self) -> bool:
        return self.gift_wrap or self.product.fragile


@dataclass(slots=True)
class Order:
    id: str
    customer: Customer
    items: list[LineItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.DRAFT
    coupon_code: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    notes: list[str] = field(default_factory=list)

    def add_item(self, item: LineItem) -> None:
        if self.status != OrderStatus.DRAFT:
            raise ValueError("cannot change a non-draft order")
        if item.quantity <= 0:
            raise ValueError("quantity must be positive")
        if not item.product.is_available():
            raise ValueError("product is not available")
        self.items.append(item)

    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)

    def subtotal_cents(self) -> int:
        return sum(item.subtotal_cents() for item in self.items)

    def has_fragile_items(self) -> bool:
        return any(item.product.fragile for item in self.items)

    def categories(self) -> set[str]:
        return {item.product.category for item in self.items}

    def iter_skus(self) -> Iterable[str]:
        for item in self.items:
            yield item.product.sku

    def confirm(self) -> None:
        if not self.items:
            raise ValueError("cannot confirm an empty order")
        self.status = OrderStatus.CONFIRMED

    def cancel(self, reason: str) -> None:
        if self.status == OrderStatus.SHIPPED:
            raise ValueError("cannot cancel shipped order")
        self.status = OrderStatus.CANCELLED
        self.notes.append(reason)
