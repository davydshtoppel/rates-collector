# Generated by Django 3.1.1 on 2020-09-20 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0012_auto_20200920_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
