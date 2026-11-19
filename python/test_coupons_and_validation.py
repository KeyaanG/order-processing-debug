from discounts import coupon_discount_amount


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def test_save10_is_ten_percent():
    result = coupon_discount_amount("SAVE10", 200)
    check(abs(result - 20.00) < 0.001, f"SAVE10 on subtotal 200 should be 20.00, got {result}")


def test_fiveoff_is_five_dollars():
    result = coupon_discount_amount("FIVEOFF", 200)
    check(abs(result - 5.00) < 0.001, f"FIVEOFF on subtotal 200 should be 5.00, got {result}")


def main():
    test_save10_is_ten_percent()
    test_fiveoff_is_five_dollars()
    print("All coupon and validation checks passed.")


if __name__ == "__main__":
    main()
