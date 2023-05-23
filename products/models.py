from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    desctiption = models.TextField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    quantity=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to='products_images')
    category=models.ForeignKey(ProductCategory, on_delete=models.CASCADE)