"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product_a():
    return Product("apple", 5, "This is an apple", 50)


@pytest.fixture
def product_b():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_cart_add_single_product(self, cart, product_b):
        product = product_b

        cart.add_product(product)
        assert cart.products[product] == 1, f"Unexpected product quantity after adding: " \
                                            f"{cart.products[product]}. Expected: 1"

        cart.add_product(product)
        assert cart.products[product] == 2, f"Unexpected product quantity after adding: " \
                                            f"{cart.products[product]}. Expected: 2"

        cart.add_product(product, 2)
        assert cart.products[product] == 4, f"Unexpected product quantity after adding: " \
                                            f"{cart.products[product]}. Expected: 4"

    def test_cart_add_products(self, cart, product_a, product_b):
        cart.add_product(product_a)
        cart.add_product(product_b)

        assert cart.products[product_a] == 1, f"Unexpected product quantity after adding: " \
                                              f"{cart.products[product_a]}. Expected: 1"
        assert cart.products[product_b] == 1, f"Unexpected product quantity after adding: " \
                                              f"{cart.products[product_b]}. Expected: 1"

        cart.add_product(product_a, 49)
        cart.add_product(product_b, 410)

        assert cart.products[product_a] == 50, f"Unexpected product quantity after adding: " \
                                               f"{cart.products[product_a]}. Expected: 50"
        assert cart.products[product_b] == 411, f"Unexpected product quantity after adding: " \
                                                f"{cart.products[product_b]}. Expected: 411"

    def test_cart_add_more_then_available(self, cart, product_a):
        product = product_a

        with pytest.raises(ValueError) as excinfo:
            cart.add_product(product, 51)
        assert f"Requested quantity of '{product.name}' is not available to adding to the cart." in str(excinfo.value)

    def test_cart_remove_product(self, cart, product_b):
        product = product_b
        cart.products[product] = 5

        cart.remove_product(product, 1)
        assert cart.products[product] == 4, f"Unexpected product quantity after removing: " \
                                            f"{cart.products[product]}. Expected: 4"

        cart.remove_product(product, 2)
        assert cart.products[product] == 2, f"Unexpected product quantity after removing: " \
                                            f"{cart.products[product]}. Expected: 2"

        cart.remove_product(product, 2)
        assert product not in cart.products, f"Product '{product.name}' " \
                                             f"was not removed from cart as expected."

        cart.products[product] = 5

        cart.remove_product(product, 6)
        assert product not in cart.products, f"Product '{product.name}' " \
                                             f"was not removed from cart as expected."

        cart.products[product] = 5

        cart.remove_product(product)
        assert product not in cart.products, f"Product '{product.name}' " \
                                             f"was not removed from cart as expected."

    def test_cart_clear(self, cart, product_a):
        product = product_a

        cart.products[product] = 5

        cart.clear()
        assert bool(cart.products) is False, f"Cart was not cleared."

    def test_cart_total_price(self, cart, product_b):
        product = product_b

        assert cart.get_total_price() == 0, "Expected cart total price to be 0 when there are no products."

        cart.products[product] = 5
        assert cart.get_total_price() == 500, f"Unexpected cart total price: {cart.get_total_price()}. " \
                                              f"Expected: 500"

        cart.remove_product(product, 2)
        assert cart.get_total_price() == 300, f"Unexpected cart total price: {cart.get_total_price()}. " \
                                              f"Expected: 300"

        cart.remove_product(product, 3)
        assert cart.get_total_price() == 0, f"Unexpected cart total price: {cart.get_total_price()}. " \
                                            f"Expected: 0"

    def test_cart_buy_single_product(self, cart, product_b):
        product = product_b

        qty = [[1, 999],
               [100, 899],
               [899, 0]]

        for q in qty:
            cart.products[product] = q[0]
            cart.buy()

            assert product.quantity == q[1], f"Unexpected product qty: {product.quantity}. " \
                                             f"Expected qty: {q[1]}"
            assert not cart.products, "Cart is not empty after buying."

    def test_cart_buy_products(self, cart, product_a, product_b):
        cart.products[product_a] = 50
        cart.products[product_b] = 10

        cart.buy()
        assert product_a.quantity == 0, f"Unexpected product qty: {product_a.quantity}. " \
                                        f"Expected qty: 0"
        assert product_b.quantity == 990, f"Unexpected product qty: {product_b.quantity}. " \
                                          f"Expected qty: 990"
        assert not cart.products, "Cart is not empty after buying."

    def test_cart_buy_more_then_available(self, cart, product_a):
        product = product_a

        cart.products[product_a] = 51

        with pytest.raises(ValueError) as excinfo:
            cart.buy()
        assert f"Requested quantity of '{product.name}' is not available to buy." in str(excinfo.value)
