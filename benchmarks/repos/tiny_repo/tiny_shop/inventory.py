"""Inventory storage and reservation logic."""

from __future__ import annotations

from dataclasses import dataclass

from tiny_shop.models import LineItem, Order, Product


@dataclass(slots=True)
class StockItem:
    product: Product
    on_hand: int
    reserved: int = 0
    reorder_point: int = 5

    @property
    def available(self) -> int:
        return max(0, self.on_hand - self.reserved)

    def should_reorder(self) -> bool:
        return self.available <= self.reorder_point


class Inventory:
    def __init__(self) -> None:
        self._stock: dict[str, StockItem] = {}

    def add_product(self, product: Product, quantity: int, reorder_point: int = 5) -> None:
        if quantity < 0:
            raise ValueError("quantity cannot be negative")
        existing = self._stock.get(product.sku)
        if existing:
            existing.on_hand += quantity
            existing.reorder_point = reorder_point
        else:
            self._stock[product.sku] = StockItem(product, quantity, reorder_point=reorder_point)

    def product(self, sku: str) -> Product:
        return self._stock[sku].product

    def has_stock(self, item: LineItem) -> bool:
        stock_item = self._stock.get(item.product.sku)
        return bool(stock_item and stock_item.available >= item.quantity)

    def reserve_order(self, order: Order) -> list[str]:
        missing = self.missing_skus(order)
        if missing:
            return missing
        for item in order.items:
            self._stock[item.product.sku].reserved += item.quantity
        return []

    def release_order(self, order: Order) -> None:
        for item in order.items:
            stock_item = self._stock.get(item.product.sku)
            if stock_item:
                stock_item.reserved = max(0, stock_item.reserved - item.quantity)

    def ship_order(self, order: Order) -> None:
        for item in order.items:
            stock_item = self._stock[item.product.sku]
            stock_item.reserved = max(0, stock_item.reserved - item.quantity)
            stock_item.on_hand = max(0, stock_item.on_hand - item.quantity)

    def missing_skus(self, order: Order) -> list[str]:
        missing = []
        for item in order.items:
            if not self.has_stock(item):
                missing.append(item.product.sku)
        return missing

    def reorder_report(self) -> list[str]:
        return [
            sku
            for sku, stock_item in sorted(self._stock.items())
            if stock_item.should_reorder()
        ]

    def snapshot(self) -> dict[str, dict[str, int]]:
        return {
            sku: {
                "on_hand": stock_item.on_hand,
                "reserved": stock_item.reserved,
                "available": stock_item.available,
            }
            for sku, stock_item in self._stock.items()
        }
