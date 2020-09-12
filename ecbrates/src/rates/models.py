from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=5, unique=True)


class Rate(models.Model):
    base_id = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='base_currency')
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency')
    value = models.DecimalField(max_digits=20, decimal_places=4)
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['base_id', 'currency_id', 'date'],
                name='unique_rate'
            ),
        ]
        indexes = [
            models.Index(fields=['date'], name='date_index'),
            models.Index(fields=['currency_id'], name='currency_index'),
        ]
