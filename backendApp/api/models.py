from django.db import models

class Stock(models.Model):
    stock_id=models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=20)
    percent_change_1hr = models.CharField(max_length=10)
    percent_change_24hr = models.CharField(max_length=10)
    percent_change_7d = models.CharField(max_length=10)
    market_cap = models.CharField(max_length=100)
    volume_24h = models.CharField(max_length=100)
    current_supply = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name