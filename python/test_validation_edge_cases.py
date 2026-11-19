from data import get_products, get_customers
from validators import validate_order


def stock_levels(products):
    return {p["id"]: p["stock"] for p in products}


def run_case(name, items, expected_errors):
    products = get_products()
    customers = get_customers()
    stock_before = stock_levels(products)
    order = {"id": 9000, "customer_id": "C002", "items": items}

    errors = validate_order(order, products, customers)

    assert errors == expected_errors, f"{name}: expected {expected_errors}, got {errors}"
    assert stock_levels(products) == stock_before, f"{name}: stock values changed during validation"
    print(f"PASS  {name}")


def main():
    # Bug #3: stock must be compared against the requested quantity, not 1
    run_case(
        "#3 Mouse qty 5 exceeds stock 4",
        [{"product_id": "P101", "quantity": 5}],
        ["Not enough inventory for Mouse"],
    )

    # Bug #4: repeated product lines must be checked against stock combined
    run_case(
        "#4 Mouse 3 + Mouse 3 exceeds stock 4",
        [{"product_id": "P101", "quantity": 3}, {"product_id": "P101", "quantity": 3}],
        ["Not enough inventory for Mouse"],
    )

    print("All validation edge cases passed.")


if __name__ == "__main__":
    main()
