"""Order orchestration services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from tiny_shop.inventory import Inventory
from tiny_shop.models import Customer, LineItem, Order, OrderStatus
from tiny_shop.pricing import PriceBreakdown, PricingEngine


@dataclass(slots=True)
class Receipt:
    order_id: str
    status: OrderStatus
    total_cents: int
    messages: list[str]


class PaymentGateway:
    def charge(self, customer: Customer, amount_cents: int) -> bool:
        if amount_cents <= 0:
            return True
        if customer.email.endswith("@declined.test"):
            return False
        return "@" in customer.email


class Mailer:
    def __init__(self) -> None:
        self.outbox: list[tuple[str, str]] = []

    def send(self, customer: Customer, subject: str) -> None:
        if customer.can_receive_promos():
            self.outbox.append((customer.email, subject))


class OrderService:
    def __init__(
        self,
        inventory: Inventory,
        pricing: PricingEngine | None = None,
        payments: PaymentGateway | None = None,
        mailer: Mailer | None = None,
    ) -> None:
        self.inventory = inventory
        self.pricing = pricing or PricingEngine()
        self.payments = payments or PaymentGateway()
        self.mailer = mailer or Mailer()
        self.orders: dict[str, Order] = {}

    def create_order(self, customer: Customer) -> Order:
        order = Order(id=uuid4().hex, customer=customer)
        self.orders[order.id] = order
        return order

    def add_sku(self, order_id: str, sku: str, quantity: int, gift_wrap: bool = False) -> None:
        order = self.orders[order_id]
        product = self.inventory.product(sku)
        order.add_item(LineItem(product, quantity, gift_wrap=gift_wrap))

    def quote(self, order_id: str) -> PriceBreakdown:
        return self.pricing.price(self.orders[order_id])

    def checkout(self, order_id: str) -> Receipt:
        order = self.orders[order_id]
        messages: list[str] = []
        if order.status != OrderStatus.DRAFT:
            return Receipt(order.id, order.status, self.quote(order_id).total_cents, ["order is not editable"])

        missing = self.inventory.reserve_order(order)
        if missing:
            messages.append("missing stock: " + ", ".join(missing))
            return Receipt(order.id, order.status, 0, messages)

        try:
            order.confirm()
            breakdown = self.pricing.price(order)
            if not self.payments.charge(order.customer, breakdown.total_cents):
                order.cancel("payment declined")
                self.inventory.release_order(order)
                messages.append("payment declined")
            else:
                messages.extend(self.fulfillment_messages(order, breakdown))
                self.mailer.send(order.customer, "Your order is confirmed")
        except Exception as exc:
            self.inventory.release_order(order)
            order.cancel(str(exc))
            messages.append("checkout failed: " + str(exc))

        return Receipt(order.id, order.status, self.quote(order_id).total_cents, messages)

    def ship(self, order_id: str) -> Receipt:
        order = self.orders[order_id]
        if order.status != OrderStatus.CONFIRMED:
            return Receipt(order.id, order.status, self.quote(order_id).total_cents, ["order is not ready"])
        self.inventory.ship_order(order)
        order.status = OrderStatus.SHIPPED
        self.mailer.send(order.customer, "Your order has shipped")
        return Receipt(order.id, order.status, self.quote(order_id).total_cents, ["shipped"])

    def cancel(self, order_id: str, reason: str) -> Receipt:
        order = self.orders[order_id]
        if order.status == OrderStatus.CONFIRMED:
            self.inventory.release_order(order)
        order.cancel(reason)
        self.mailer.send(order.customer, "Your order was cancelled")
        return Receipt(order.id, order.status, self.quote(order_id).total_cents, [reason])

    def fulfillment_messages(self, order: Order, breakdown: PriceBreakdown) -> list[str]:
        messages = []
        if breakdown.discount_cents:
            messages.append(f"discount applied: {breakdown.discount_cents}")
        if breakdown.credit_cents:
            messages.append(f"store credit used: {breakdown.credit_cents}")
        if order.has_fragile_items():
            messages.append("fragile handling requested")
        if order.item_count() > 8:
            messages.append("large order packed in multiple boxes")
        if order.customer.country != "US":
            messages.append("international shipping")
        return messages

    def stale_drafts(self, max_age_days: int) -> list[Order]:
        stale = []
        for order in self.orders.values():
            age_days = (datetime.now(UTC) - order.created_at).days
            if order.status == OrderStatus.DRAFT and age_days > max_age_days:
                stale.append(order)
        return stale
