from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def check_quantity_available(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return True if self.quantity >= int(quantity) else False

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity_available(quantity):
            self.quantity -= quantity
        else:
            raise ValueError(f"Requested quantity of '{self.name}' is not available.")

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def check_product_in_cart(self, product: Product) -> bool:
        return True if product in self.products else False

    def add_product(self, product: Product, quantity=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product.check_quantity_available(quantity):
            if self.check_product_in_cart(product):
                self.products[product] += quantity
            else:
                self.products[product] = quantity
        else:
            raise ValueError(f"Requested quantity of '{product.name}' "
                             f"is not available to adding to the cart.")

    def remove_product(self, product: Product, quantity=None):
        """
        Метод удаления продукта из корзины.
        Если quantity не передан, то удаляется вся позиция
        Если quantity больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if self.check_product_in_cart(product):
            if quantity is None or quantity >= self.products[product]:
                del self.products[product]
            else:
                self.products[product] -= quantity

    def clear(self):
        self.products = {}

    def get_total_price(self) -> float:
        total: float = 0

        for product in self.products:
            total += product.price * self.products[product]

        return total

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product in self.products:
            if not product.check_quantity_available(self.products[product]):
                raise ValueError(f"Requested quantity of '{product.name}' is not available to buy.")

        for product in self.products:
            product.quantity -= self.products[product]

        self.clear()
