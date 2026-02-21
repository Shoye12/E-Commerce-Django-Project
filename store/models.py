from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=200, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.first_name}'s Cart - {self.product.name}"

    @property
    def total_cost(self):
        return self.quantity * self.product.price

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    customer_name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.user.first_name}"

    @property
    def total_cost(self):
        return self.quantity * self.product.price
