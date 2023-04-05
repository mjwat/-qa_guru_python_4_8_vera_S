"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        qty = [0, 1, 1000]
        qty_neg = [1001, 1000000000]

        for q in qty:
            assert product.check_quantity_available(q) is True, f"Test failed: {product.name} should be available. " \
                                                      f"Salable Quantity is {product.quantity}. " \
                                                      f"Requested {q}."

        for q in qty_neg:
            assert product.check_quantity_available(q) is False, f"Test failed: The requested qty should not be available " \
                                                       f"for '{product.name}' product. " \
                                                       f"Salable Quantity is {product.quantity}. " \
                                                       f"Requested {q}."

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(1)
        assert product.quantity == 999, f"Unexpected product quantity after buying: " \
                                        f"{product.quantity}. Expected: 999"

        product.buy(5)
        assert product.quantity == 994, f"Unexpected product quantity after buying: " \
                                        f"{product.quantity}. Expected: 944"

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError) as excinfo:
            product.buy(1001)
        assert f"Requested quantity of '{product.name}' is not available." in str(excinfo.value)
