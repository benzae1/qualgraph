"""Pricing rules for orders."""

from __future__ import annotations

from dataclasses import dataclass

from tiny_shop.models import CustomerTier, Order


@dataclass(slots=True)
class PriceBreakdown:
    subtotal_cents: int
    discount_cents: int
    tax_cents: int
    shipping_cents: int
    credit_cents: int

    @property
    def total_cents(self) -> int:
        return max(
            0,
            self.subtotal_cents
            - self.discount_cents
            + self.tax_cents
            + self.shipping_cents
            - self.credit_cents,
        )


class PricingEngine:
    def __init__(self, tax_rates: dict[str, float] | None = None) -> None:
        self.tax_rates = tax_rates or {"US": 0.075, "DE": 0.19, "GB": 0.2}

    def price(self, order: Order) -> PriceBreakdown:
        subtotal = order.subtotal_cents()
        discount = self.discount_for(order, subtotal)
        taxable = self.taxable_subtotal(order, discount)
        tax = self.tax_for(order.customer.country, taxable)
        shipping = self.shipping_for(order)
        credit = self.credit_for(order, subtotal + tax + shipping - discount)
        return PriceBreakdown(
            subtotal_cents=subtotal,
            discount_cents=discount,
            tax_cents=tax,
            shipping_cents=shipping,
            credit_cents=credit,
        )

    def discount_for(self, order: Order, subtotal_cents: int) -> int:
        discount = self.tier_discount(order.customer.tier, subtotal_cents)
        discount += self.coupon_discount(order.coupon_code, subtotal_cents)
        discount += self.category_discount(order, subtotal_cents)
        return min(discount, subtotal_cents)

    def tier_discount(self, tier: CustomerTier, subtotal_cents: int) -> int:
        if tier == CustomerTier.STAFF:
            return subtotal_cents // 2
        if tier == CustomerTier.GOLD:
            return subtotal_cents // 10
        if tier == CustomerTier.SILVER:
            return subtotal_cents // 20
        return 0

    def coupon_discount(self, coupon_code: str | None, subtotal_cents: int) -> int:
        if not coupon_code:
            return 0
        normalized = coupon_code.strip().upper()
        if normalized == "WELCOME10":
            return min(1000, subtotal_cents // 10)
        if normalized == "SHIPFREE":
            return 0
        if normalized.startswith("SAVE"):
            try:
                dollars = int(normalized.removeprefix("SAVE"))
            except ValueError:
                return 0
            return min(dollars * 100, subtotal_cents // 3)
        return 0

    def category_discount(self, order: Order, subtotal_cents: int) -> int:
        categories = order.categories()
        if "clearance" in categories:
            return subtotal_cents // 4
        if {"books", "stationery"}.issubset(categories):
            return 500
        if order.item_count() >= 10:
            return subtotal_cents // 20
        return 0

    def taxable_subtotal(self, order: Order, discount_cents: int) -> int:
        taxable = sum(
            item.subtotal_cents()
            for item in order.items
            if item.product.taxable
        )
        if taxable == 0:
            return 0
        discount_ratio = discount_cents / max(order.subtotal_cents(), 1)
        return round(taxable * (1 - discount_ratio))

    def tax_for(self, country: str, taxable_cents: int) -> int:
        rate = self.tax_rates.get(country.upper(), self.tax_rates["US"])
        return round(taxable_cents * rate)

    def shipping_for(self, order: Order) -> int:
        if order.coupon_code and order.coupon_code.upper() == "SHIPFREE":
            return 0
        if order.subtotal_cents() >= 7500:
            return 0
        base = 799 if order.customer.country == "US" else 1899
        if order.has_fragile_items():
            base += 350
        if order.item_count() > 5:
            base += 250
        return base

    def credit_for(self, order: Order, balance_cents: int) -> int:
        if not order.customer.has_credit():
            return 0
        return min(order.customer.store_credit_cents, max(0, balance_cents))
