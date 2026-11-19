from data import get_products
from discounts import coupon_discount_amount
from orders import calculate_subtotal

# Bug: coupon codes ignore surrounding whitespace and don't crash on non-strings
assert coupon_discount_amount(" save10 ", 200) != 0, "padded coupon not recognized"
assert coupon_discount_amount(123, 200) == 0, "non-string coupon should give no discount"

# Bug: subtotal is price * quantity
products = get_products()
price = next(p["price"] for p in products if p["id"] == "P100")
order = {"items": [{"product_id": "P100", "quantity": 2}]}
assert calculate_subtotal(order, products) == round(price * 2, 2), "subtotal should be price * quantity"

print("All order/discount edge cases passed.")