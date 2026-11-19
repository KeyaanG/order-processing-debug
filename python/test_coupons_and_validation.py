from data import get_products, get_customers, get_tax_rates
from discounts import coupon_discount_amount
from orders import process_order
from validators import validate_order


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def test_save10_is_ten_percent():
    result = coupon_discount_amount("SAVE10", 200)
    check(abs(result - 20.00) < 0.001, f"SAVE10 on subtotal 200 should be 20.00, got {result}")


def test_fiveoff_is_five_dollars():
    result = coupon_discount_amount("FIVEOFF", 200)
    check(abs(result - 5.00) < 0.001, f"FIVEOFF on subtotal 200 should be 5.00, got {result}")


def test_items_none_gives_validation_error():
    order = {"id": 2001, "customer_id": "C001", "coupon": None, "items": None}
    errors = validate_order(order, get_products(), get_customers())
    check("Order must contain at least one item" in errors, f"items=None should give a validation error, got {errors}")


def test_invalid_order_does_not_change_stock():
    products = get_products()
    order = {"id": 3001, "customer_id": "C002", "coupon": None, "items": [{"product_id": "P103", "quantity": 2}]}
    result = process_order(order, products, get_customers(), get_tax_rates())
    stock = next(p for p in products if p["id"] == "P103")["stock"]
    check(result["valid"] is False, "Order for an out-of-stock item should be invalid")
    check(stock == 0, f"Invalid order must not change stock, P103 stock is {stock}")
    check(result["total"] == 0, f"Invalid order should not be charged, total is {result['total']}")


def test_unknown_customer_is_rejected():
    order = {"id": 3002, "customer_id": "C999", "coupon": None, "items": [{"product_id": "P100", "quantity": 1}]}
    result = process_order(order, get_products(), get_customers(), get_tax_rates())
    check(result["valid"] is False, "Unknown customer should make the order invalid")
    check("Customer does not exist" in result["errors"], f"Expected a customer error, got {result['errors']}")


def main():
    test_save10_is_ten_percent()
    test_fiveoff_is_five_dollars()
    test_items_none_gives_validation_error()
    test_invalid_order_does_not_change_stock()
    test_unknown_customer_is_rejected()
    print("All coupon and validation checks passed.")


if __name__ == "__main__":
    main()
