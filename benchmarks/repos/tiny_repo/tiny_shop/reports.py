"""Reporting helpers for the tiny shop benchmark."""

from __future__ import annotations

from collections import Counter, defaultdict

from tiny_shop.inventory import Inventory
from tiny_shop.models import Order, OrderStatus
from tiny_shop.orders import OrderService


def revenue_by_country(orders: list[Order], service: OrderService) -> dict[str, int]:
    revenue: dict[str, int] = defaultdict(int)
    for order in orders:
        if order.status in {OrderStatus.CONFIRMED, OrderStatus.SHIPPED}:
            revenue[order.customer.country] += service.pricing.price(order).total_cents
    return dict(revenue)


def popular_categories(orders: list[Order], limit: int = 5) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for order in orders:
        for item in order.items:
            counts[item.product.category] += item.quantity
    return counts.most_common(limit)


def customer_summary(service: OrderService) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = {}
    for order in service.orders.values():
        email = order.customer.email
        current = summary.setdefault(email, {"orders": 0, "items": 0, "spend": 0})
        current["orders"] += 1
        current["items"] += order.item_count()
        if order.status != OrderStatus.CANCELLED:
            current["spend"] += service.pricing.price(order).total_cents
    return summary


def inventory_health(inventory: Inventory) -> dict[str, object]:
    snapshot = inventory.snapshot()
    low_stock = inventory.reorder_report()
    total_available = sum(item["available"] for item in snapshot.values())
    total_reserved = sum(item["reserved"] for item in snapshot.values())
    return {
        "sku_count": len(snapshot),
        "low_stock": low_stock,
        "total_available": total_available,
        "total_reserved": total_reserved,
    }


def render_daily_digest(service: OrderService, inventory: Inventory) -> str:
    orders = list(service.orders.values())
    revenue = revenue_by_country(orders, service)
    categories = popular_categories(orders)
    health = inventory_health(inventory)
    lines = [
        "# Daily digest",
        "",
        "Revenue:",
        *[f"- {country}: {cents / 100:.2f}" for country, cents in sorted(revenue.items())],
        "",
        "Popular categories:",
        *[f"- {name}: {count}" for name, count in categories],
        "",
        f"Low stock SKUs: {', '.join(health['low_stock']) or 'none'}",
        f"Available units: {health['total_available']}",
        f"Reserved units: {health['total_reserved']}",
    ]
    return "\n".join(lines)
