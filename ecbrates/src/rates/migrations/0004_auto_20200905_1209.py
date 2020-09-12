# Generated by Django 3.1.1 on 2020-09-05 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0003_auto_20200905_1156'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='rate',
            index=models.Index(fields=['date'], name='date_index'),
        ),
        migrations.AddIndex(
            model_name='rate',
            index=models.Index(fields=['currency_id'], name='currency_index'),
        ),
    ]
