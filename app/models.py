from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    product_image = models.ImageField()

    # Другие поля, если нужно

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Order(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='OrderProduct', through_fields=('order', 'product'), related_name='orders')

    def total(self):
        total_price = 0
        total_quantity = 0
        order_products = OrderProduct.objects.filter(order=self)
        for order_product in order_products:
            total_price += order_product.subtotal
            total_quantity += order_product.quantity
        return {'price': total_price, 'quantity': total_quantity}

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def get_total_price(self):
        if self.price is None:
            return None
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.quantity -= self.quantity
        self.product.save()

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f'{self.quantity} x {self.product.name} (${self.price})'
