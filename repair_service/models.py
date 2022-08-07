from django.conf import settings
from django.db import models


class Request(models.Model):

    STATUS_CHOICES = [
        ("Ready", "Ready"),
        ("In work", "In work"),
        ("In line", "In line"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_model = models.CharField(max_length=255, null=True)
    problem_description = models.TextField(null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="In line")

    def __str__(self):
        return f"Request id: {self.id}, ({self.user}, {self.status})"


class Invoice(models.Model):

    request = models.ForeignKey("Request", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.request}, {self.price}"

