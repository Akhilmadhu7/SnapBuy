# Generated by Django 4.0.6 on 2022-07-20 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category_adminside', '0006_remove_category_mobile_category_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newcart', '0005_alter_cartitem_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customername', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=120)),
                ('address', models.TextField(max_length=600)),
                ('city', models.CharField(max_length=200)),
                ('pincode', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=120)),
                ('country', models.CharField(max_length=120)),
                ('total_price', models.CharField(max_length=100)),
                ('tax', models.CharField(max_length=120)),
                ('shippping', models.CharField(max_length=100)),
                ('grandtotal', models.CharField(max_length=120)),
                ('paymentmode', models.CharField(max_length=120)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('Out for shipping', 'Out for shipping'), ('Completed', 'Completed')], default='pending', max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newcart.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category_adminside.product')),
            ],
        ),
    ]