from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#3498db") # Hex color for charts

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    source_file = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"
