from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=55)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.PositiveIntegerField(default=0)
    create_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
