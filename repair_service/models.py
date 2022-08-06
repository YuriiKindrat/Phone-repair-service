from django.conf import settings
from django.db import models


class Request(models.Model):

    STATUS_CHOICES = [
        ("R", "Ready"),
        ("W", "In work"),
        ("L", "In line"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_model = models.CharField(max_length=255)
    problem_description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="L")

    def __str__(self):
        return f"{self.id}, ({self.user}, {self.status})"


class Invoice(models.Model):

    request = models.ForeignKey("Request", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField()

    def __str__(self):
        return f"{self.request}, {self.price}"

