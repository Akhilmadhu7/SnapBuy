# Generated by Django 4.0.6 on 2022-07-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0011_alter_cartproduct_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='subtotal',
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='rate',
            field=models.PositiveIntegerField(default=0),
        ),
    ]