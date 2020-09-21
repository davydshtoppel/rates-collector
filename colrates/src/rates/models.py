from django.db import models


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=5, unique=True)


class Rate(models.Model):
    id = models.AutoField(primary_key=True)
    base = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='base_currency')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency')
    value = models.DecimalField(max_digits=20, decimal_places=4)
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['base', 'currency', 'date'],
                name='unique_rate'
            ),
        ]
        indexes = [
            models.Index(fields=['date'], name='date_index'),
            models.Index(fields=['currency'], name='currency_index'),
        ]
