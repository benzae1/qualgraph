from tiny_shop.inventory import Inventory
from tiny_shop.models import Customer, CustomerTier, Product
from tiny_shop.orders import Mailer, OrderService, PaymentGateway
from tiny_shop.pricing import PricingEngine
from tiny_shop.reports import inventory_health, popular_categories


def make_inventory() -> Inventory:
    inventory = Inventory()
    inventory.add_product(Product("BOOK-1", "Notebook", 1200, "books"), 12)
    inventory.add_product(Product("PEN-1", "Pen", 250, "stationery"), 100)
    inventory.add_product(Product("MUG-1", "Mug", 1800, "home", fragile=True), 4)
    inventory.add_product(Product("CLR-1", "Old calendar", 500, "clearance"), 2)
    return inventory


def test_checkout_reserves_stock_and_sends_mail() -> None:
    inventory = make_inventory()
    mailer = Mailer()
    service = OrderService(inventory, mailer=mailer)
    order = service.create_order(Customer("c-1", "ada@example.com", CustomerTier.GOLD))

    service.add_sku(order.id, "BOOK-1", 2)
    service.add_sku(order.id, "PEN-1", 3)
    receipt = service.checkout(order.id)

    assert receipt.status.value == "confirmed"
    assert receipt.total_cents > 0
    assert inventory.snapshot()["BOOK-1"]["reserved"] == 2
    assert mailer.outbox == [("ada@example.com", "Your order is confirmed")]


def test_checkout_reports_missing_stock() -> None:
    inventory = make_inventory()
    service = OrderService(inventory)
    order = service.create_order(Customer("c-2", "grace@example.com"))

    service.add_sku(order.id, "MUG-1", 8)
    receipt = service.checkout(order.id)

    assert receipt.status.value == "draft"
    assert receipt.total_cents == 0
    assert "missing stock: MUG-1" in receipt.messages


def test_payment_decline_releases_stock() -> None:
    inventory = make_inventory()
    service = OrderService(inventory, payments=PaymentGateway())
    order = service.create_order(Customer("c-3", "bad@declined.test"))

    service.add_sku(order.id, "BOOK-1", 1)
    receipt = service.checkout(order.id)

    assert receipt.status.value == "cancelled"
    assert receipt.messages == ["payment declined"]
    assert inventory.snapshot()["BOOK-1"]["reserved"] == 0


def test_pricing_combines_coupon_and_category_discount() -> None:
    inventory = make_inventory()
    service = OrderService(inventory, pricing=PricingEngine({"US": 0.1}))
    order = service.create_order(Customer("c-4", "lin@example.com", store_credit_cents=300))

    service.add_sku(order.id, "BOOK-1", 1)
    service.add_sku(order.id, "PEN-1", 1)
    order.coupon_code = "WELCOME10"

    quote = service.quote(order.id)

    assert quote.discount_cents >= 500
    assert quote.tax_cents > 0
    assert quote.credit_cents == 300


def test_reports_summarize_categories_and_inventory() -> None:
    inventory = make_inventory()
    service = OrderService(inventory)
    order = service.create_order(Customer("c-5", "katherine@example.com"))
    service.add_sku(order.id, "BOOK-1", 2)
    service.add_sku(order.id, "PEN-1", 1)

    assert popular_categories([order]) == [("books", 2), ("stationery", 1)]
    assert inventory_health(inventory)["sku_count"] == 4
