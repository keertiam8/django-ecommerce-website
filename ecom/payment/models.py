from django.db import models
from django.contrib.auth.models import User
from store.models import Product, Profile
from django.db.models.signals import post_save


# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f"Shipping Address - {str(self.id)}"
    
    
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()
post_save.connect(create_shipping, sender=User)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=500, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order - {str(self.id)}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    

    def __str__(self):
        return f"OrderItem - {str(self.id)}"